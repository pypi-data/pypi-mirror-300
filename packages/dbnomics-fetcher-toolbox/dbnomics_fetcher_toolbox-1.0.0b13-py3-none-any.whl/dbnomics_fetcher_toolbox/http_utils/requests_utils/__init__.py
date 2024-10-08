from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from requests import Session

from dbnomics_fetcher_toolbox.sentinels import UNINITIALIZED, Uninitialized

from .helper import RequestsHelper

if TYPE_CHECKING:
    from tenacity import BaseRetrying


__all__ = ["download_http_url", "fetch_http_url"]


def download_http_url(
    url: str,
    *,
    output_file: Path,
    response_dump_dir: Path | None = None,
    retrying: "BaseRetrying | Uninitialized | None" = UNINITIALIZED,
    session: Session | None = None,
    user_agent: str | Literal[False] | None = None,
) -> None:
    response_dump_file = None
    if response_dump_dir is not None:
        response_dump_dir.mkdir(exist_ok=True, parents=True)
        response_dump_file = response_dump_dir / f"{output_file.name}.response.txt"

    helper = RequestsHelper(
        url,
        retrying=retrying,
        session=session,
        user_agent=user_agent,
    )
    return helper.download(output_file, response_dump_file=response_dump_file)


def fetch_http_url(
    url: str,
    *,
    response_dump_file: Path | None = None,
    retrying: "BaseRetrying | Uninitialized | None" = UNINITIALIZED,
    session: Session | None = None,
    user_agent: str | Literal[False] | None = None,
) -> Iterator[bytes]:
    source = RequestsHelper(
        url,
        retrying=retrying,
        session=session,
        user_agent=user_agent,
    )
    return source.iter_bytes(response_dump_file=response_dump_file)
