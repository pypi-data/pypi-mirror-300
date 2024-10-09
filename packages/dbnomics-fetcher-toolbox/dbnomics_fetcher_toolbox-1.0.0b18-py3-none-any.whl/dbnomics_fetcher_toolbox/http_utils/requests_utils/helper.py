import codecs
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Final, Literal, TypeVar

import daiquiri
import requests
import requests_toolbelt.utils.dump
from humanfriendly import format_timespan
from requests import Response, Session
from requests.exceptions import RequestException
from tenacity import AttemptManager

from dbnomics_fetcher_toolbox._internal.file_utils import replace_all_extensions
from dbnomics_fetcher_toolbox.file_utils import write_chunks
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.sentinels import UNINITIALIZED, Uninitialized

from .retry import default_retrying

if TYPE_CHECKING:
    from requests.api import _HeadersMapping  # type: ignore[reportPrivateUsage]
    from requests.sessions import _Params, _Timeout  # type: ignore[reportPrivateUsage]
    from tenacity import BaseRetrying


__all__ = ["RequestsHelper"]


logger = daiquiri.getLogger(__name__)

T = TypeVar("T")


default_timeout: Final = timedelta(minutes=1)
default_user_agent: Final = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"


class RequestsHelper:
    def __init__(
        self,
        url: str,
        *,
        chunk_size: int | None = None,
        connect_timeout: float | timedelta | None = None,
        decoder_errors: str | None = None,
        encoding: str | None = None,
        headers: "_HeadersMapping | None" = None,
        method: str | None = None,
        params: "_Params | None" = None,
        read_timeout: float | timedelta | None = None,
        retrying: "BaseRetrying | Uninitialized | None" = UNINITIALIZED,
        session: Session | None = None,
        stream: bool = True,
        use_response_charset: bool | str = True,
        user_agent: str | Literal[False] | None = None,
    ) -> None:
        def normalize_timeout(timeout: float | timedelta | None) -> float:
            if timeout is None:
                # Avoid doing a request without timeout, because it could take an infinite time if the server has no timeout.
                return default_timeout.total_seconds()

            if isinstance(timeout, timedelta):
                return timeout.total_seconds()

            return timeout

        self.chunk_size = chunk_size
        self.connect_timeout = normalize_timeout(connect_timeout)

        if decoder_errors is None:
            decoder_errors = "strict"
        self.decoder_errors = decoder_errors

        if encoding is None:
            encoding = "utf-8"
        self.encoding = encoding

        self.headers = headers
        self.method = method
        self.params = params
        self.read_timeout = normalize_timeout(read_timeout)

        if isinstance(retrying, Uninitialized):
            retrying = default_retrying
        self._retrying = retrying

        self.stream = stream
        self.url = url
        self.use_response_charset = use_response_charset

        if user_agent is None:
            user_agent = default_user_agent
        elif user_agent is False:
            user_agent = None
        self._user_agent = user_agent

        self._session = session

    def download(self, output_file: Path, *, response_dump_file: Path | None) -> None:
        if self._retrying is None:
            bytes_iter = self._iter_bytes_attempt(response_dump_file=response_dump_file)
            write_chunks(bytes_iter, output_file=output_file)

        else:
            for attempt in self._retrying:
                if response_dump_file is not None:
                    response_dump_file = self._update_response_dump_file(response_dump_file, attempt=attempt)
                with attempt:
                    bytes_iter = self._iter_bytes_attempt(response_dump_file=response_dump_file)
                    write_chunks(bytes_iter, output_file=output_file)

                outcome = attempt.retry_state.outcome
                assert outcome is not None
                if not outcome.failed:
                    attempt.retry_state.set_result(output_file)

    def iter_bytes(self, *, response_dump_file: Path | None) -> Iterator[bytes]:
        if self._retrying is None:
            yield from self._iter_bytes_attempt(response_dump_file=response_dump_file)

        else:
            for attempt in self._retrying:
                if response_dump_file is not None:
                    response_dump_file = self._update_response_dump_file(response_dump_file, attempt=attempt)
                with attempt:
                    yield from self._iter_bytes_attempt(response_dump_file=response_dump_file)

    def _fetch_url(
        self,
        url: str,
        *,
        headers: "_HeadersMapping | None" = None,
        method: str | None = None,
        params: "_Params | None" = None,
        response_dump_file: Path | None = None,
        session: Session | None = None,
        stream: bool = True,
        timeout: "_Timeout",
    ) -> Response:
        if method is None:
            method = "get"

        request_func = requests.request if session is None else session.request

        if self._user_agent is not None:
            if headers is None:
                headers = {}
            headers = {"User-Agent": self._user_agent, **headers}

        response = request_func(method, url, headers=headers, params=params, stream=stream, timeout=timeout)

        try:
            response.raise_for_status()
        except RequestException:
            if response_dump_file is not None:
                self._save_http_response_dump(response, output_file=response_dump_file)
            raise

        if response_dump_file is not None:
            self._save_http_response_dump(response, output_file=response_dump_file)

        return response

    def _iter_bytes_attempt(self, *, response_dump_file: Path | None) -> Iterator[bytes]:
        logger.debug(
            "Fetching URL %r (connect timeout: %s, read timeout: %s)%s...",
            self.url,
            format_timespan(self.connect_timeout),
            format_timespan(self.read_timeout),
            "" if self._retrying is not None else " without any retry strategy",
            params=self.params,
        )

        response = self._fetch_url(
            self.url,
            headers=self.headers,
            method=self.method,
            params=self.params,
            response_dump_file=response_dump_file,
            session=self._session,
            stream=self.stream,
            timeout=(self.connect_timeout, self.read_timeout),
        )

        logger.debug("Received HTTP response: %r", response)

        use_response_charset = self.use_response_charset
        content_iter = response.iter_content(chunk_size=self.chunk_size)
        if use_response_charset is True and response.encoding is not None:
            content_iter = self._reencode(content_iter, from_encoding=response.encoding)
        elif isinstance(use_response_charset, str):
            content_iter = self._reencode(content_iter, from_encoding=use_response_charset)
        return content_iter

    def _reencode(self, content_iter: Iterator[bytes], *, from_encoding: str) -> Iterator[bytes]:
        decoder = codecs.getincrementaldecoder(from_encoding)(errors=self.decoder_errors)

        for chunk in content_iter:
            decoded_chunk = decoder.decode(chunk)
            if decoded_chunk:
                yield decoded_chunk.encode(self.encoding)
        decoded_chunk = decoder.decode(b"", final=True)
        if decoded_chunk:
            yield decoded_chunk.encode(self.encoding)

    def _save_http_response_dump(self, response: Response, *, output_file: Path) -> None:
        response_dump = requests_toolbelt.utils.dump.dump_all(response)
        output_file.write_bytes(response_dump)
        logger.debug("Dumped response to %s", format_file_path_with_size(output_file))

    def _update_response_dump_file(self, response_dump_file: Path, *, attempt: AttemptManager) -> Path:
        return replace_all_extensions(
            response_dump_file,
            [
                *response_dump_file.suffixes[:-1],
                f".attempt_{attempt.retry_state.attempt_number}",
                response_dump_file.suffixes[-1],
            ],
        )
