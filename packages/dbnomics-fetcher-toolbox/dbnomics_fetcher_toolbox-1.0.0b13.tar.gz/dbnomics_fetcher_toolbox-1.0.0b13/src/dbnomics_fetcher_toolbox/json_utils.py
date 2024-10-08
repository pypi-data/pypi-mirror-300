import os
import subprocess
from pathlib import Path

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size

__all__ = ["reformat_json_file"]


logger = daiquiri.getLogger(__name__)


def reformat_json_file(json_file: Path, *, indent_level: int = 2) -> None:
    tmp_file = json_file.with_suffix(".tmp.json")
    jq_cmd = os.getenv("JQ_PATH", default="/usr/bin/jq")
    with Timer() as timer:
        try:
            output = subprocess.check_output(  # noqa: S602
                f"{jq_cmd} --indent {indent_level} < {json_file} > {tmp_file}",
                shell=True,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            logger.error("Error reformatting JSON file, jq stderr: %s", exc.stderr.decode("utf-8"))  # noqa: TRY400
            raise
    tmp_file.rename(json_file)
    stdout = output.decode("utf-8")
    log_msg = "Reformatted JSON file %s"
    if stdout:
        log_msg += f"jq stdout: {stdout}"
    logger.debug(
        log_msg,
        format_file_path_with_size(json_file),
        duration=format_timer(timer),
    )
