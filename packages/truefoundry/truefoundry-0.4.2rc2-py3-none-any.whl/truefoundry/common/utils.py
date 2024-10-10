import os
import time
from functools import lru_cache, wraps
from time import monotonic_ns
from typing import Callable, Generator, Optional, TypeVar
from urllib.parse import urljoin, urlsplit

from truefoundry.common.constants import (
    API_SERVER_RELATIVE_PATH,
    SERVICEFOUNDRY_SERVER_URL_ENV_KEY,
    TFY_HOST_ENV_KEY,
)

T = TypeVar("T")


def relogin_error_message(message: str, host: str = "HOST") -> str:
    suffix = ""
    if host == "HOST":
        suffix = " where HOST is TrueFoundry platform URL"
    return (
        f"{message}\n"
        f"Please login again using `tfy login --host {host} --relogin` "
        f"or `truefoundry.login(host={host!r}, relogin=True)` function" + suffix
    )


def timed_lru_cache(
    seconds: int = 300, maxsize: Optional[int] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def wrapper_cache(func: Callable[..., T]) -> Callable[..., T]:
        func = lru_cache(maxsize=maxsize)(func)
        func.delta = seconds * 10**9
        func.expiration = monotonic_ns() + func.delta

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if monotonic_ns() >= func.expiration:
                func.cache_clear()
                func.expiration = monotonic_ns() + func.delta
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def poll_for_function(
    func: Callable[..., T], poll_after_secs: int = 5, *args, **kwargs
) -> Generator[T, None, None]:
    while True:
        yield func(*args, **kwargs)
        time.sleep(poll_after_secs)


def validate_tfy_host(tfy_host: str) -> str:
    if not (tfy_host.startswith("https://") or tfy_host.startswith("http://")):
        raise ValueError(
            f"Invalid host {tfy_host!r}. It should start with https:// or http://"
        )


def resolve_tfy_host(tfy_host: Optional[str] = None) -> str:
    if not tfy_host and not os.getenv(TFY_HOST_ENV_KEY):
        raise ValueError(
            f"Either `host` should be provided using `--host <value>`, or `{TFY_HOST_ENV_KEY}` env must be set"
        )
    tfy_host = tfy_host or os.getenv(TFY_HOST_ENV_KEY)
    tfy_host = tfy_host.strip("/")
    validate_tfy_host(tfy_host)
    return tfy_host


# TODO (chiragjn): Rename base_url to tfy_host
def append_servicefoundry_path_to_base_url(base_url: str):
    if urlsplit(base_url).netloc.startswith("localhost"):
        return os.getenv(SERVICEFOUNDRY_SERVER_URL_ENV_KEY)
    return urljoin(base_url, API_SERVER_RELATIVE_PATH)
