import os
import subprocess
from pathlib import Path

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size

__all__ = ["normalize_sdmx_file_header"]


logger = daiquiri.getLogger(__name__)


def normalize_sdmx_file_header(sdmx_file: Path, *, tag_names: list[str]) -> None:
    """Normalize SDMX header in-place by replacing the text of child elements that change too often.

    Example:
    -------
        - before: <mes:Prepared>2024-09-27T17:12:02.793+02:00</mes:Prepared>
        - after: <mes:Prepared>REDACTED</mes:Prepared>

    This is specifically useful to avoid creating false revisions of the file.

    """
    # Check file existence manually because `perl -i` does not fail if file is missing.
    if not sdmx_file.is_file():
        raise FileNotFoundError(sdmx_file)

    with Timer() as timer:
        tag_names_str = "|".join(tag_names)
        perl_script = r"""
            BEGIN { $count = 0; }
            if ($count < tag_names_len && /<(tag_names_str)>/) {
                s/(<.+>).*(<.+>)/\1REDACTED\2/;
                $count++;
            }
        """.replace("tag_names_len", str(len(tag_names))).replace("tag_names_str", tag_names_str)
        try:
            output = subprocess.check_output(  # noqa: S603
                [
                    os.getenv("PERL_PATH", default="/usr/bin/perl"),
                    "-i",
                    "-pe",
                    perl_script,
                    str(sdmx_file),
                ],
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Error normalizing the header of SDMX file, stderr: %s", exc.stderr.decode("utf-8"))  # noqa: TRY400
            raise

    stdout = output.decode("utf-8")
    log_msg = "Normalized the header of SDMX file %s"
    if stdout:
        log_msg += f"stdout: {stdout}"
    logger.debug(log_msg, format_file_path_with_size(sdmx_file), duration=format_timer(timer))
