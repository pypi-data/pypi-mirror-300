import os
import subprocess
from itertools import chain
from pathlib import Path

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size

__all__ = ["normalize_sdmx_file_header"]


logger = daiquiri.getLogger(__name__)


def normalize_sdmx_file_header(
    sdmx_file: Path,
    *,
    replacement_text: str = "REDACTED",
    xpaths: list[str],
) -> None:
    """Normalize SDMX header in-place by replacing the text of child elements that change too often.

    Example:
    -------
        - before: <mes:Prepared>2024-09-27T17:12:02.793+02:00</mes:Prepared>
        - after: <mes:Prepared>REDACTED</mes:Prepared>

    This is specifically useful to avoid creating false revisions of the file.

    """
    if not sdmx_file.is_file():
        raise FileNotFoundError(sdmx_file)

    logger.debug("Normalizing the header of SDMX file %s", format_file_path_with_size(sdmx_file))

    command = [
        os.getenv("XMLSTARLET_PATH", default="/usr/bin/xmlstarlet"),
        "edit",
        *chain.from_iterable(["--update", xpath, "--value", replacement_text] for xpath in xpaths),
        str(sdmx_file),
    ]
    tmp_file = sdmx_file.with_stem(f"{sdmx_file.stem}.tmp")

    with Timer() as timer:
        try:
            with tmp_file.open("w") as f:
                subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=f)  # noqa: S603
        except subprocess.CalledProcessError as exc:
            logger.error("Error normalizing the header of SDMX file, stderr: %s", exc.stderr.decode("utf-8"))  # noqa: TRY400
            raise

        tmp_file.rename(sdmx_file)

    logger.debug(
        "Normalized the header of SDMX file %s",
        format_file_path_with_size(sdmx_file),
        duration=format_timer(timer),
    )
