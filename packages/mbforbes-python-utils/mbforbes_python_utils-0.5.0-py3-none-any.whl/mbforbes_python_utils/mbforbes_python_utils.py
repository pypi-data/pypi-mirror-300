"""Python utils."""

import argparse
import os
from typing import Any, Callable


def display_args(args: argparse.Namespace, display: Callable[[str], None] = print):
    """Displays parsed `args` (defaults to `print`, pass anything that takes `str`.)"""
    display("")
    display("Arguments:")
    arg_width = max(len(arg) for arg in vars(args))
    for arg in vars(args):
        value = getattr(args, arg)
        display(f"{arg.ljust(arg_width)}: {value} [{type(value).__name__}]")
    display("")


# def flatten(lst):
#     """Generator version. Consider adding this at some point."""
#     for el in lst:
#         if isinstance(el, list):
#             yield from flatten(el)
#         else:
#             yield el


def flatten(lst: list[Any]) -> list[Any]:
    """Flattens list of any depth to a single list."""
    result = []
    for el in lst:
        if isinstance(el, list):
            result.extend(flatten(el))  # type: ignore
        else:
            result.append(el)  # type: ignore
    return result  # type: ignore


def read(path: str) -> str:
    """Returns contents of file at `path`, leading/trailing whitespace stripped."""
    with open(os.path.expanduser(path), "r") as f:
        return f.read().strip()


def write(path: str, contents: str, info_print: bool = True) -> None:
    """Writes `contents` to `path`, makes dirs if needed, prints info msg w/ path."""
    dirname = os.path.dirname(path)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w") as f:
        f.write(contents)
    if info_print:
        print('Wrote {} chars to "{}"'.format(len(contents), path))
