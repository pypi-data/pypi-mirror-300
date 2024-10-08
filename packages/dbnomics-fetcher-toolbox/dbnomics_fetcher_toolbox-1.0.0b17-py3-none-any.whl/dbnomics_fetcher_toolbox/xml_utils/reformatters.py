import os
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

import daiquiri
from contexttimer import Timer
from humanfriendly import format_size
from iterable_subprocess import iterable_subprocess

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size

__all__ = ["reformat_xml_file", "reformat_xml_stream"]


logger = daiquiri.getLogger(__name__)


def reformat_xml_file(xml_file: Path, *, indent_level: int = 2) -> None:
    tmp_file = xml_file.with_suffix(".tmp.xml")
    with Timer() as timer:
        try:
            output = subprocess.check_output(  # noqa: S603
                [
                    _get_xmlindent_command(),
                    "-i",
                    str(indent_level),
                    str(xml_file),
                    "-o",
                    str(tmp_file),
                ],
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Error reformatting XML file, stderr: %s", exc.stderr.decode("utf-8"))  # noqa: TRY400
            raise

    initial_file_size = format_size(xml_file.stat().st_size, binary=True)
    tmp_file.rename(xml_file)
    stdout = output.decode("utf-8")
    log_msg = "Reformatted XML file %s"
    if stdout:
        log_msg += f"stdout: {stdout}"
    logger.debug(
        log_msg,
        format_file_path_with_size(xml_file),
        duration=format_timer(timer),
        initial_file_size=initial_file_size,
    )


@contextmanager
def reformat_xml_stream(xml_chunks: Iterator[bytes], *, indent_level: int = 2) -> Iterator[Iterator[bytes]]:
    with iterable_subprocess(
        [
            _get_xmlindent_command(),
            "-f",  # force indenting elements without children
            "-i",
            str(indent_level),
        ],
        xml_chunks,
    ) as output:
        yield output


def _get_xmlindent_command() -> str:
    return os.getenv("XMLINDENT_PATH", default="/usr/bin/xmlindent")
