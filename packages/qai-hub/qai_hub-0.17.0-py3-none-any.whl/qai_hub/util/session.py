from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import List, Protocol, TypeVar

import backoff
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import qai_hub

# Will sleep {backoff factor} * (2 ** ({number of previous retries})) seconds
BACKOFF_FACTOR = 0.75
# Try 6 times total, for a max total delay of about 20s
MAX_RETRIES = 5
# The maximum length of any single wait (this is here mainly for testing)
MAX_WAIT = 10

# How long to wait for data before timing out a connected socket.
# Our webserver is configured to timeout requests after 25 seconds,
# so we specify a slightly higher max timeout for all requests.
# By default, requests waits forever.
# https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts
READ_TIMEOUT = 28

RETRIABLE_STATUSES = [
    429,  # Too many requests
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
]


# Matches the response objects from both "requests" and "httpx"
class GenericHTTPResponse(Protocol):
    @property
    def status_code(self) -> int:
        ...


def is_retriable_status(response: GenericHTTPResponse):
    return response.status_code in RETRIABLE_STATUSES


HTTPResponseLike = TypeVar("HTTPResponseLike", bound=GenericHTTPResponse)


def retry_with_backoff(
    additional_exceptions_to_retry: List[type[Exception]] = [],
) -> Callable[[Callable[..., HTTPResponseLike]], Callable[..., HTTPResponseLike]]:
    """
    Decorator for retrying functions that need to set up state as well as make an HTTP call.
    Assumes the function will return a response object with a `status_code` attribute,
    and may raise connect and timeout exceptions from the `requests` library or the additional
    exception types provided.

    The user of this decorator is responsible for making sure the call is safe to retry.
    """

    def wrapper(
        func: Callable[..., HTTPResponseLike]
    ) -> Callable[..., HTTPResponseLike]:
        @functools.wraps(func)
        @backoff.on_exception(
            wait_gen=backoff.expo,
            exception=(
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            )
            + tuple(additional_exceptions_to_retry),
            max_tries=1 + MAX_RETRIES,
            factor=BACKOFF_FACTOR,
            max_value=MAX_WAIT,
        )
        @backoff.on_predicate(
            wait_gen=backoff.expo,
            max_tries=1 + MAX_RETRIES,
            predicate=is_retriable_status,
            factor=BACKOFF_FACTOR,
            max_value=MAX_WAIT,
        )
        def inner(*args, **kwargs) -> HTTPResponseLike:
            return func(*args, **kwargs)

        return inner

    return wrapper


def retry_call_with_backoff(func: Callable[[], HTTPResponseLike]) -> HTTPResponseLike:
    """
    Retry a single call to a no-arg function, as in @retry_with_backoff.
    """

    @functools.wraps(func)
    @retry_with_backoff()
    def inner() -> HTTPResponseLike:
        return func()

    return inner()


class LogRetry(Retry):
    """
    Adding extra logs before making a retry request
    """

    def increment(self, *args, **kwargs):
        retry_object = super().increment(*args, **kwargs)

        url_log = f" for {kwargs['url']}" if kwargs.get("url") else ""
        error_log = f"; error was {kwargs['error']}" if kwargs.get("error") else ""

        # Total is the number of retries remaining. Starts at MAX_RETRIES and counts down to zero.
        if self.total < MAX_RETRIES:
            logging.info(
                f"Retry attempt number {MAX_RETRIES - self.total}{url_log}{error_log}"
            )

        return retry_object


class SessionWithRetryAndTimeout(requests.Session):
    def request(self, *args, **kwargs) -> requests.Response:
        default_kwargs = {"timeout": READ_TIMEOUT}

        return super().request(*args, **{**default_kwargs, **kwargs})


def create_session() -> SessionWithRetryAndTimeout:
    """
    Get a requests.Session object pre-configured to do safe retries and time out all requests.
    "Safe to retry" includes failure to connect with any HTTP method, or a retriable
    HTTP status or read timeout from an idempotent HTTP method (GET, PUT, DELETE, HEAD, OPTIONS).
    """
    session = SessionWithRetryAndTimeout()
    session.headers.update({"User-Agent": f"qai_hub/{qai_hub.__version__}"})
    retries = LogRetry(
        total=MAX_RETRIES,
        # Enable exponential back-off
        backoff_factor=BACKOFF_FACTOR,
        # Retry for these statuses
        status_forcelist=RETRIABLE_STATUSES,
        # Retry on connection errors
        connect=MAX_RETRIES,
        # Retry on read errors
        read=MAX_RETRIES,
        # Don't retry on redirect (default)
        redirect=None,
        # Retry on errors other than connection, read, redirect or status.
        other=MAX_RETRIES,
    )

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session
