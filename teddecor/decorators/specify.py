"""teddecor.decorators.specify

This module aims to create decorators that specify what something is.
For example the depricated decorator prints a deprication warning to stderr
while not_implemented raises a not implemented error. The decorators aim
to give more context information to methods and classes.
"""

from typing import Callable
from sys import stderr
from inspect import signature
from teddecor.TED import TED
from utility import parse_signature
from teddecor.logger import Logger

__all__ = ["not_implemented", "deprecated"]


def parse_qual_name(qual_name: str) -> str:
    qual_name = qual_name.split(".")
    if len(qual_name) > 1:
        return (
            "*"
            + ".".join([f"[@F #f5a97f]{val}[@F]" for val in qual_name[:-1]])
            + f".[@F #8aadf4]{qual_name[-1]}[@F]*"
        )
    else:
        return f"*[@F #8aadf4]{qual_name[0]}[@F]*"


def parse_bases(cls) -> str:
    bases = [base.__name__ for base in cls.__bases__ if base.__name__ != "object"]
    return f"[@F #ee99a0]([@F]{', '.join([f'[@F #f5a97f]{val}[@F]'] for val in bases)}[@F #ee99a0])[@F]"


def not_implemented(obj: Callable | type):
    """Raise a not implemented error for a specific method or class."""

    if isinstance(obj, Callable) and not isinstance(obj, type):

        def inner(*args, **kwargs):
            raise NotImplementedError(
                TED.parse(
                    f"*[@F #8aadf4]{obj.__name__}[@F]{parse_signature(obj)} is not yet implemented"
                )
            )

        return inner

    if isinstance(obj, type):

        class Inner:  # pylint: disable=too-few-public-methods
            """The innter class to not implemented error. Replicates passed
            in class but raises a not implemented error if the class is used/initialized."""

            def __init__(self, *args, **kwargs):
                raise NotImplementedError(
                    TED.parse(
                        f"*Class [@F #f5a97f]{obj.__name__}[@F] is not yet implemented"
                    )
                )

        return Inner


def deprecated(obj: Callable | type):
    """Write to stderr that a specific method is deprecated."""

    if isinstance(obj, Callable) and not isinstance(obj, type):

        def inner(*args, **kwargs):
            Logger.custom(
                TED.parse(f"{parse_qual_name(obj.__qualname__)}{parse_signature(obj)}"),
                label="Deprecated[@F].[@F #ed8796]def",
                clr="#eed49f",
            )
            Logger.flush()
            return obj(*args, **kwargs)

        return inner

    if isinstance(obj, type):

        class Inner(obj):  # pylint: disable=too-few-public-methods
            """The innter class to deprecation. Replicates passed
            in class but calls stderr with a deprecation message."""

            def __init__(self, *args, **kwargs):
                Logger.custom(
                    TED.parse(
                        f"[@F #f5a97f]*{obj.__name__}*[@F]{parse_bases(obj)}"
                    ),
                    label="Deprecated[@F].[@F #ed8796]class",
                    clr="#eed49f",
                )
                Logger.flush()
                super().__init__(*args, **kwargs)

        return Inner
