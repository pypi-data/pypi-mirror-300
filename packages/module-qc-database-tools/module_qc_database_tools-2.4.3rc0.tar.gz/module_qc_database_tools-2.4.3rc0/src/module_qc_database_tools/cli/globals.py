from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path

import typer

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class LogLevel(str, Enum):
    """
    Enum for log levels.
    """

    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


OPTIONS = {}


def verbosity_callback(ctx: typer.Context, value: LogLevel):
    """
    Callback to set log level at the package-level.
    """
    if ctx.resilient_parsing:
        return None

    logging.getLogger("module_qc_database_tools").setLevel(value.value)
    return value


OPTIONS["verbosity"]: LogLevel = typer.Option(
    LogLevel.info,
    "-v",
    "--verbosity",
    help="Log level [options: DEBUG, INFO (default) WARNING, ERROR]",
    callback=verbosity_callback,
)
OPTIONS["measurement_path"]: Path = typer.Option(
    "Measurement/",
    "-p",
    "--path",
    help="Path to directory with output measurement files",
    exists=True,
    file_okay=True,
    readable=True,
    writable=True,
    resolve_path=True,
)
OPTIONS["host"]: str = typer.Option("localhost", "--host", help="localDB server")
OPTIONS["port"]: int = typer.Option(
    5000,
    "--port",
    help="localDB port",
)
OPTIONS["dry_run"]: bool = typer.Option(
    False,
    "-n",
    "--dry-run",
    help="Dry-run, do not submit to localDB or update controller config.",
)
OPTIONS["output_path"]: Path = typer.Option(
    "tmp.json",
    "--out",
    "--output-path",
    help="Analysis output result json file path to save in the local host",
    exists=False,
    writable=True,
)
