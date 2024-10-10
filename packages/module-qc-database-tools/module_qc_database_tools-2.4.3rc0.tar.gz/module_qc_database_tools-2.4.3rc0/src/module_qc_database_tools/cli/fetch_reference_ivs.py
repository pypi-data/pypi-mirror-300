from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

import jsbeautifier
import typer
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rich import print as rich_print

from module_qc_database_tools.cli.utils import get_itkdb_client
from module_qc_database_tools.iv import fetch_reference_ivs

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})
log = logging.getLogger(__name__)


@app.command()
def main(
    serial_number: str = typer.Option(..., "-sn", "--sn", help="ATLAS serial number"),
    output_file: Optional[Path] = typer.Option(  # noqa: UP007
        None,
        "-o",
        "--output-file",
        help="Path to file. If not specified, will print to stdout.",
        exists=False,
        writable=True,
        dir_okay=False,
    ),
    mongo_uri: str = typer.Option(
        "mongodb://localhost:27017/localdb",
        "-u",
        "--uri",
        help="mongo URI (see documentation for mongo client)",
    ),
    localdb_name: str = typer.Option(
        "localdb",
        "-d",
        "--dbname",
        help="database name used for localDB. This is in your localDB config either as --db (command-line) or as mongoDB.db (yaml).",
    ),
    ssl: bool = typer.Option(
        None, "--ssl/--no-ssl", help="Use ssl for the connection to mongoDB"
    ),
    itkdb_access_code1: Optional[str] = typer.Option(  # noqa: UP007
        None, "--accessCode1", help="Access Code 1 for production DB"
    ),
    itkdb_access_code2: Optional[str] = typer.Option(  # noqa: UP007
        None, "--accessCode2", help="Access Code 2 for production DB"
    ),
    localdb: bool = typer.Option(
        False,
        "--localdb/--proddb",
        help="Whether to pull from localDB (default) or from Production DB.",
    ),
    reference_component_type: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "-c",
        "--reference-component-type",
        help="Component Type to use as reference",
    ),
    reference_stage: Optional[str] = typer.Option(  # noqa: UP007
        None, "-s", "--reference-stage", help="Stage to use as reference"
    ),
    reference_test_type: Optional[str] = typer.Option(  # noqa: UP007
        None, "-t", "--reference-test-type", help="Test Type to use as reference"
    ),
    mongo_serverSelectionTimeoutMS: int = typer.Option(
        5,
        "--serverSelectionTimeoutMS",
        help="server selection timeout in seconds",
    ),
):
    """
    Main executable for fetching reference IVs from either production DB (default) or local DB.

    !!! note "Added in version 2.3.0"

    """
    if localdb:
        kwargs = {"serverSelectionTimeoutMS": mongo_serverSelectionTimeoutMS * 1000}
        if ssl is not None:
            kwargs["ssl"] = ssl

        mongo_client = MongoClient(mongo_uri, **kwargs)
        try:
            db_names = mongo_client.list_database_names()
        except ConnectionFailure as exc:
            rich_print("[red]Unable to connect to mongoDB[/]")
            raise typer.Exit(1) from exc

        if localdb_name not in db_names:
            rich_print(
                f"[red][underline]{localdb_name}[/underline] not in [underline]{db_names}[/underline][/red]."
            )
            raise typer.Exit(1)

        client = mongo_client[localdb_name]
    else:
        client = get_itkdb_client(
            access_code1=itkdb_access_code1, access_code2=itkdb_access_code2
        )

    try:
        reference_ivs = fetch_reference_ivs(
            client,
            serial_number,
            reference_component_type=reference_component_type,
            reference_stage=reference_stage,
            reference_test_type=reference_test_type,
        )
    except ValueError as exc:
        rich_print(f":warning: [red bold]Error[/]: {exc}")
        raise typer.Exit(2) from exc

    json_data = json.dumps(reference_ivs, sort_keys=True)
    options = jsbeautifier.default_options()
    options.indent_size = 4
    pretty_json_data = jsbeautifier.beautify(json_data, options)

    if output_file:
        output_file.write_text(pretty_json_data)
        msg = f"Written to {output_file:s}"
        log.info(msg)
    else:
        rich_print(pretty_json_data)


if __name__ == "__main__":
    typer.run(main)
