from typing import Never
from . import bpftrace
from . import perfetto


def panic(msg: str) -> Never:
    import typer

    msg = msg.strip()
    if not msg.lower().startswith("error:"):
        msg = f"ERROR: {msg}"
    typer.secho(msg, fg=typer.colors.RED, err=True)
    raise typer.Exit(code=1)


def get_rest_args() -> list[str] | None:
    import sys

    if "--" in sys.argv:
        return sys.argv[sys.argv.index("--") + 1 :]

    return None
