import subprocess

import typer
from rich import print
from rich.padding import Padding


def abort(s):
    header = color("Exiting... ", "red")
    message(header + s, padding="around")
    raise typer.Abort()


def message(the_message, padding=None, indent: int = 0):
    if indent:
        the_message = Padding.indent(the_message, indent)

    if padding == "around":
        the_message = Padding(the_message, pad=(1, 2, 1, 2))
    elif padding == "above":
        the_message = Padding(the_message, pad=(1, 2, 0, 2))
    elif padding == "below":
        the_message = Padding(the_message, pad=(0, 2, 1, 2))

    print(the_message)


def color(s, color):
    return f"[bold {color}]{s}[/]"


def cmd(args):
    return subprocess.run(args, check=True, capture_output=True, encoding="utf-8")
