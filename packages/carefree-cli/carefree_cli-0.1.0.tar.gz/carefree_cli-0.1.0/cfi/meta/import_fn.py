import json

from typer import Argument
from pathlib import Path
from typing_extensions import Annotated

from .. import console
from .export_fn import Template
from ..crud.create import add


def import_fn(
    file: Annotated[
        str,
        Argument(help=("Path of the file to import the templates from.\n\n")),
    ],
) -> None:
    file_path = Path(file)
    with file_path.open("r") as f:
        templates_json = json.load(f)
    templates = [Template(**t) for t in templates_json]
    for template in templates:
        add(template.cmd, str(template.hierarchy), verbose=False)
    console.log(f"imported {len(templates)} templates from '{file_path}'!")
