from filelock import FileLock

from .. import console
from ..utils import ask_with_warn
from ..utils import parse_hierarchy_path
from ..common import hierarchy_argument
from ..common import template_argument


def add(
    template: template_argument,
    hierarchy: hierarchy_argument,
    *,
    verbose: bool = True,
) -> None:
    template_path = parse_hierarchy_path(hierarchy)
    with FileLock(template_path.with_suffix(".lock")):
        if template_path.exists():
            if not ask_with_warn(
                f"Template '{template_path}' already exists, do you want to overwrite it?"
            ):
                console.error("Then please choose another hierarchy.")
                return None
        template_path.write_text(template)
        if verbose:
            console.log(f"""'{template}' is saved to '{template_path}'.""")
