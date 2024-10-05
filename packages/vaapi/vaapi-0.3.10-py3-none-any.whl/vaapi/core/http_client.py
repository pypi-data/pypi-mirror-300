import asyncio
import email.utils
import json
import re
import time
import typing
import urllib.parse
from contextlib import asynccontextmanager, contextmanager
from random import random

import httpx

from .file import File, convert_file_dict_to_httpx_tuples
from .jsonable_encoder import jsonable_encoder
from .query_encoder import encode_query
from .remove_none_from_dict import remove_none_from_dict
from .request_options import RequestOptions

INITIAL_RETRY_DELAY_SECONDS = 0.5
MAX_RETRY_DELAY_SECONDS = 10
MAX_RETRY_DELAY_SECONDS_FROM_HEADER = 30


def _parse_retry_after(response_headers: httpx.Headers) -> typing.Optional[float]:
    """
    This function parses the `Retry-After` header in a HTTP response and returns the number of seconds to wait.

    Inspired by the urllib3 retry implementation.
    """
    retry_after_ms = response_headers.get("retry-after-ms")
    if retry_after_ms is not None:
        try:
            return int(retry_after_ms) / 1000 if retry_after_ms > 0 else 0
        except Exception:
            pass

    retry_after = response_headers.get("retry-after")
    if retry_after is None:
        return None

    # Attempt to parse the header as an int.
    if re.match(r"^\s*[0-9]+\s*$", retry_after):
        seconds = float(retry_after)
    # Fallback to parsing it as a date.
    else:
        retry_date_tuple = email.utils.parsedate_tz(retry_after)
        if retry_date_tuple is None:
            return None
        if retry_date_tuple[9] is None:  # Python 2
            # Assume UTC if no timezone was specified
            # On Python2.7, parsedate_tz returns None for a timezone offset
            # instead of 0 if no timezone is given, where mktime_tz treats
            # a None timezone offset as local time.
            retry_date_tuple = retry_date_tuple[:9] + (0,) + retry_date_tuple[10:]

        retry_date = email.utils.mktime_tz(retry_date_tuple)
        seconds = retry_date - time.time()

    if seconds < 0:
        seconds = 0

    return seconds


def _retry_timeout(response: httpx.Response, retries: int) -> float:
    """
    Determine the amount of time to wait before retrying a request.
    This function begins by trying to parse a retry-after header from the response, and then proceeds to use exponential backoff
    with a jitter to determine the number of seconds to wait.
    """

    # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
    retry_after = _parse_retry_after(response.headers)
    if retry_after is not None and retry_after <= MAX_RETRY_DELAY_SECONDS_FROM_HEADER:
        return retry_after

    # Apply exponential backoff, capped at MAX_RETRY_DELAY_SECONDS.
    retry_delay = min(INITIAL_RETRY_DELAY_SECONDS * pow(2.0, retries), MAX_RETRY_DELAY_SECONDS)

    # Add a randomness / jitter to the retry delay to avoid overwhelming the server with retries.
    timeout = retry_delay * (1 - 0.25 * random())
    return timeout if timeout >= 0 else 0


def _should_retry(response: httpx.Response) -> bool:
    retriable_400s = [429, 408, 409]
    return response.status_code >= 500 or response.status_code in retriable_400s


def remove_omit_from_dict(
    original: typing.Dict[str, typing.Optional[typing.Any]], omit: typing.Optional[typing.Any]
) -> typing.Dict[str, typing.Any]:
    if omit is None:
        return original
    new: typing.Dict[str, typing.Any] = {}
    for key, value in original.items():
        if value is not omit:
            new[key] = value
    return new


def maybe_filter_request_body(
    data: typing.Optional[typing.Any],
    request_options: typing.Optional[RequestOptions],
    omit: typing.Optional[typing.Any],
) -> typing.Optional[typing.Any]:
    if data is None:
        return (
            jsonable_encoder(request_options.get("additional_body_parameters", {}))
            if request_options is not None
            else None
        )
    elif not isinstance(data, typing.Mapping):
        data_content = jsonable_encoder(data)
    else:
        data_content = {
            **(jsonable_encoder(remove_omit_from_dict(data, omit))),  # type: ignore
            **(
                jsonable_encoder(request_options.get("additional_body_parameters", {}))
                if request_options is not None
                else {}
            ),
        }
    return data_content


# Abstracted out for testing purposes
def get_request_body(
    *,
    json: typing.Optional[typing.Any],
    data: typing.Optional[typing.Any],
    request_options: typing.Optional[RequestOptions],
    omit: typing.Optional[typing.Any],
) -> typing.Tuple[typing.Optional[typing.Any], typing.Optional[typing.Any]]:
    json_body = None
    data_body = None
    if data is not None:
        data_body = maybe_filter_request_body(data, request_options, omit)
    else:
        # If both data and json are None, we send json data in the event extra properties are specified
        json_body = maybe_filter_request_body(json, request_options, omit)

    return json_body, data_body


class HttpClient:
    def __init__(
        self,
        *,
        httpx_client: httpx.Client,
        base_timeout: typing.Optional[float],
        base_headers: typing.Dict[str, str],
        base_url: typing.Optional[str] = None,
    ):
        self.base_url = base_url
        self.base_timeout = base_timeout
        self.base_headers = base_headers
        self.httpx_client = httpx_client

    def get_base_url(self, maybe_base_url: typing.Optional[str]) -> str:
        base_url = self.base_url if maybe_base_url is None else maybe_base_url
        if base_url is None:
            raise ValueError("A base_url is required to make this request, please provide one and try again.")
        return base_url

    def request(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]]] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 0,
        omit: typing.Optional[typing.Any] = None,
    ) -> httpx.Response:
        base_url = self.get_base_url(base_url)
        timeout = (
            request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self.base_timeout
        )

        json_body, data_body = get_request_body(json=json, data=data, request_options=request_options, omit=omit)

        response = self.httpx_client.request(
            method=method,
            url=urllib.parse.urljoin(f"{base_url}/", path),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self.base_headers,
                        **(headers if headers is not None else {}),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            params=encode_query(
                jsonable_encoder(
                    remove_none_from_dict(
                        remove_omit_from_dict(
                            {
                                **(params if params is not None else {}),
                                **(
                                    request_options.get("additional_query_parameters", {})
                                    if request_options is not None
                                    else {}
                                ),
                            },
                            omit,
                        )
                    )
                )
            ),
            json=json_body,
            data=data_body,
            content=content,
            files=convert_file_dict_to_httpx_tuples(remove_none_from_dict(files)) if files is not None else None,
            timeout=timeout,
        )

        max_retries: int = request_options.get("max_retries", 0) if request_options is not None else 0
        if _should_retry(response=response):
            if max_retries > retries:
                time.sleep(_retry_timeout(response=response, retries=retries))
                return self.request(
                    path=path,
                    method=method,
                    base_url=base_url,
                    params=params,
                    json=json,
                    content=content,
                    files=files,
                    headers=headers,
                    request_options=request_options,
                    retries=retries + 1,
                    omit=omit,
                )

        return response

    @contextmanager
    def stream(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]]] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 0,
        omit: typing.Optional[typing.Any] = None,
    ) -> typing.Iterator[httpx.Response]:
        base_url = self.get_base_url(base_url)
        timeout = (
            request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self.base_timeout
        )

        json_body, data_body = get_request_body(json=json, data=data, request_options=request_options, omit=omit)

        with self.httpx_client.stream(
            method=method,
            url=urllib.parse.urljoin(f"{base_url}/", path),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self.base_headers,
                        **(headers if headers is not None else {}),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            params=encode_query(
                jsonable_encoder(
                    remove_none_from_dict(
                        remove_omit_from_dict(
                            {
                                **(params if params is not None else {}),
                                **(
                                    request_options.get("additional_query_parameters", {})
                                    if request_options is not None
                                    else {}
                                ),
                            },
                            omit,
                        )
                    )
                )
            ),
            json=json_body,
            data=data_body,
            content=content,
            files=convert_file_dict_to_httpx_tuples(remove_none_from_dict(files)) if files is not None else None,
            timeout=timeout,
        ) as stream:
            yield stream


class AsyncHttpClient:
    def __init__(
        self,
        *,
        httpx_client: httpx.AsyncClient,
        base_timeout: typing.Optional[float],
        base_headers: typing.Dict[str, str],
        base_url: typing.Optional[str] = None,
    ):
        self.base_url = base_url
        self.base_timeout = base_timeout
        self.base_headers = base_headers
        self.httpx_client = httpx_client

    def get_base_url(self, maybe_base_url: typing.Optional[str]) -> str:
        base_url = self.base_url if maybe_base_url is None else maybe_base_url
        if base_url is None:
            raise ValueError("A base_url is required to make this request, please provide one and try again.")
        return base_url

    async def request(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]]] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 0,
        omit: typing.Optional[typing.Any] = None,
    ) -> httpx.Response:
        base_url = self.get_base_url(base_url)
        timeout = (
            request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self.base_timeout
        )

        json_body, data_body = get_request_body(json=json, data=data, request_options=request_options, omit=omit)

        # Add the input to each of these and do None-safety checks
        response = await self.httpx_client.request(
            method=method,
            url=urllib.parse.urljoin(f"{base_url}/", path),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self.base_headers,
                        **(headers if headers is not None else {}),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            params=encode_query(
                jsonable_encoder(
                    remove_none_from_dict(
                        remove_omit_from_dict(
                            {
                                **(params if params is not None else {}),
                                **(
                                    request_options.get("additional_query_parameters", {})
                                    if request_options is not None
                                    else {}
                                ),
                            },
                            omit,
                        )
                    )
                )
            ),
            json=json_body,
            data=data_body,
            content=content,
            files=convert_file_dict_to_httpx_tuples(remove_none_from_dict(files)) if files is not None else None,
            timeout=timeout,
        )

        max_retries: int = request_options.get("max_retries", 0) if request_options is not None else 0
        if _should_retry(response=response):
            if max_retries > retries:
                await asyncio.sleep(_retry_timeout(response=response, retries=retries))
                return await self.request(
                    path=path,
                    method=method,
                    base_url=base_url,
                    params=params,
                    json=json,
                    content=content,
                    files=files,
                    headers=headers,
                    request_options=request_options,
                    retries=retries + 1,
                    omit=omit,
                )
        return response

    @asynccontextmanager
    async def stream(
        self,
        path: typing.Optional[str] = None,
        *,
        method: str,
        base_url: typing.Optional[str] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        json: typing.Optional[typing.Any] = None,
        data: typing.Optional[typing.Any] = None,
        content: typing.Optional[typing.Union[bytes, typing.Iterator[bytes], typing.AsyncIterator[bytes]]] = None,
        files: typing.Optional[typing.Dict[str, typing.Optional[typing.Union[File, typing.List[File]]]]] = None,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
        request_options: typing.Optional[RequestOptions] = None,
        retries: int = 0,
        omit: typing.Optional[typing.Any] = None,
    ) -> typing.AsyncIterator[httpx.Response]:
        base_url = self.get_base_url(base_url)
        timeout = (
            request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self.base_timeout
        )

        json_body, data_body = get_request_body(json=json, data=data, request_options=request_options, omit=omit)

        async with self.httpx_client.stream(
            method=method,
            url=urllib.parse.urljoin(f"{base_url}/", path),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self.base_headers,
                        **(headers if headers is not None else {}),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            params=encode_query(
                jsonable_encoder(
                    remove_none_from_dict(
                        remove_omit_from_dict(
                            {
                                **(params if params is not None else {}),
                                **(
                                    request_options.get("additional_query_parameters", {})
                                    if request_options is not None
                                    else {}
                                ),
                            },
                            omit=omit,
                        )
                    )
                )
            ),
            json=json_body,
            data=data_body,
            content=content,
            files=convert_file_dict_to_httpx_tuples(remove_none_from_dict(files)) if files is not None else None,
            timeout=timeout,
        ) as stream:
            yield stream