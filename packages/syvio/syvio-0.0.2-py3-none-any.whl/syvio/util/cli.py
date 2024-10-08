import typer
import numpy as np
from rich import print
from rich.panel import Panel

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

APP = typer.Typer(
    no_args_is_help=True, add_completion=False, context_settings=CONTEXT_SETTINGS
)


def __plot_get_bin_counts(values: list[float]):
    bins = [0] * 41
    for v in values:
        if v < 1:
            bins[0] += 1
        elif v >= 2**41:
            bins[-1] += 1
        else:
            bins[int(np.log2(v))] += 1
    return bins


def __plot_label(v: int):
    v = int(v)

    v = int(v)
    if v < 1024:
        x = v
        y = f""
    elif v < 1024 * 1024:
        x = int(v / 1024)
        y = "K"
    elif v < 1024 * 1024 * 1024:
        x = int(v / 1024 / 1024)
        y = "M"
    else:
        x = int(v / 1024 / 1024 / 1024)
        y = "G"
    count = len(f"{x} {y}".strip())
    return f"[bold bright_cyan]{x}[/bold bright_cyan] {y}".strip(), count


def plot_hist(name: str, values: list[float]):
    bins = __plot_get_bin_counts(values)
    assert len(bins) == 41, f"len(bins) = {len(bins)}"
    total = sum(bins)
    rows: list[tuple[str, str, str, int]] = []
    for i in range(40):
        count = bins[i]
        ratio = count / total
        lo, c1 = __plot_label(2**i)
        hi, c2 = __plot_label(2 ** (i + 1))
        label = f"[{lo}, {hi})"
        pad = 15 - c1 - c2 - 4
        label += " " * pad
        rows.append((label, f"{count}", "█" * int(np.ceil(ratio * 50)), count))
    lo, c = __plot_label(2**40)
    ratio = bins[-1] / total
    label = f"[{lo},"
    pad = 15 - c - 2
    label += " " * pad
    rows.append((label, f"{bins[-1]}", "█" * int(np.ceil(ratio * 50)), bins[-1]))
    # Remove leading and trailing rows with count = 0
    for i in range(len(rows)):
        if rows[i][3] != 0:
            rows = rows[i:]
            break
    for i in range(len(rows) - 1, -1, -1):
        if rows[i][3] != 0:
            rows = rows[: i + 1]
            break
    content = ""
    for row in rows:
        content += f"{row[0]:<15} [bold bright_cyan]{row[1]:>10}[/bold bright_cyan] | {row[2]:<50} |\n"
    content += (
        f"\n[bold]{'Total':<15}[/bold] [bold bright_cyan]{total:>10}[/bold bright_cyan]"
    )
    print(
        Panel.fit(
            content,
            title=f"[bold bright_cyan]{name}[/bold bright_cyan]",
            title_align="left",
            padding=(1, 1),
        )
    )
