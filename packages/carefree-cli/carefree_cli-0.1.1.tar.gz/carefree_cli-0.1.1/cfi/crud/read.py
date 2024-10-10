import subprocess

import regex as re

from typer import Option
from typing import List
from typing import NamedTuple
from typing_extensions import Annotated

from .. import console
from ..utils import parse_hierarchy_path
from ..common import hierarchy_argument


class Parsed(NamedTuple):
    to_fill: List[str]
    template: str


def parse(template: str) -> Parsed:
    """
    parse a given `template`. each `template` should have three formats:
    * plain command, i.e. the direct command to run. no '{}'s.
    * placeholder template, which is a string with some '{}'s, each '{}' can either
      have a name included not not.
    > if no name, should use '__i' as the name, where `__i` is the index of the '{}'.
    """
    to_fill = []
    no_names = []
    for i, m in enumerate(re.finditer(r"\{([^}]*)\}", template)):
        i_name = m.group(1)
        if i_name:
            to_fill.append(i_name)
        else:
            no_names.append(i)
            to_fill.append(f"__{i}")
            template = template[: m.start()] + f"__{{{i}}}" + template[m.end() :]
    return Parsed(to_fill=to_fill, template=template)


def load(
    hierarchy: hierarchy_argument,
    run_command: Annotated[
        bool,
        Option(
            "--run/--dry",
            help="Whether to run the command (with `subprocess.run`) or just print it.",
        ),
    ] = True,
) -> None:
    template_path = parse_hierarchy_path(hierarchy)
    if not template_path.exists():
        console.error(f"Cannot find template at '{template_path}'.")
        return None
    template = template_path.read_text()
    parsed = parse(template)
    if not parsed.to_fill:
        template = parsed.template
    else:
        kwargs = {}
        console.log(f"filling command '{parsed.template}'")
        for to_fill in parsed.to_fill:
            value = console.ask(f"[cyan]`{to_fill}`")
            kwargs[to_fill] = value
        template = parsed.template.format(**kwargs)
    if not run_command:
        console.log("command loaded, copy-paste as you like!")
        console.log(f"[green]{template}")
    else:
        q = f"""command loaded as [green]'{template}'[/green], run it?"""
        if console.ask(q, ["y", "n"], default="y") == "y":
            subprocess.run(template, shell=True, check=True)
