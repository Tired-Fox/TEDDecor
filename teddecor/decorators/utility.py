"""teddecor.decorators.utility

This modules provides decorators that provide utility. This includes
decorators that time execution, prints debug information, and much more.
"""

from time import monotonic
from typing import Callable
from sys import stdout
from inspect import signature, _empty
from teddecor.TED import TED
from teddecor.logger import Log, LL

from teddecor.pprint import p_value

__all__ = ["Time", "debug", "parse_signature"]

logger = Log(level=LL.DEBUG)


def Time(func: Callable):
    """Time a given function execution and write the results to stdout."""
    # Method: def {signature(func)}
    def time_inner(*args, **kwargs):
        start = monotonic()
        result = func(*args, **kwargs)
        final = monotonic() - start
        stdout.write(
            f"""
Time: {final}s
Method: {func.__name__}
"""
        )
        stdout.flush()
        return result

    return time_inner


def parse_signature(obj: Callable) -> str:
    """Parse and format the signature of a function."""

    values = []
    for key, value in signature(obj).parameters.items():
        # value = Parameter
        if str(value.kind) != "POSITIONAL_OR_KEYWORD":
            t = (
                "[@F #91d7e3]\\*[@F]"
                if str(value.kind) == "VAR_POSITIONAL"
                else "[@F #91d7e3]\\*\\*[@F]"
            )
        else:
            t = ""
        a = (
            f": [@F #f5a97f]{value.annotation.__name__}[@F]"
            if value.default is not _empty
            else ""
        )
        n = f"[@F #f5bde6]{TED.encode(value.name)}[@F]"
        d = (
            f" [@F #7dc4e4]=[@F] {p_value(value.default, decode=False)}"
            if value.default is not _empty
            else ""
        )
        values.append(f"{t}{n}{a}{d}")

    # Parse signature return types
    ra = str(signature(obj).return_annotation)

    if "|" in ra:
        from re import finditer

        rvalues = []
        for _type in finditer(r"(\s?\|\s+)?([a-zA-Z]+)", ra):

            if _type in ["None", "NoneType"]:
                rvalues.append(p_value(None, decode=False))
            else:
                rvalues.append(f"[@F #f5a97f]{TED.encode(_type.group(2))}[@F]")
        return_anno = " | ".join(rvalues)
    else:
        from re import match, split

        def parse_types(type_anno: str) -> list:
            _, name, types = match(r"^(typing.)?([A-Za-z]+)\[(.+)+\]$", type_anno).groups()
            rtypes = []

            for _type in [val for val in split(r"(, )(?![a-zA-Z, _.]+\])", types) if val != ", "]:
                if _type in ["None", "NoneType"]:
                    rtypes.append(p_value(None, decode=False))
                elif "[" in _type:
                    rtypes.append(parse_types(_type))
                else:
                    rtypes.append(
                        f"[@F #f5a97f]{TED.encode(_type.split('.')[-1])}[@F]"
                    )

            return f"[@F #f5a97f]{TED.encode(name)}[@F]\\[{', '.join(rtypes)}\\]"

        return_anno = parse_types(ra)

    # Construct colored signature
    return f"[@F #ee99a0]([@F]{', '.join(values)}[@F #ee99a0])[@F] -> {return_anno}"


def debug(depth: int = 1):
    """Debug the taken args and kwargs along with dispaying the results"""

    def decorator(obj: Callable | type):
        def debug_wrapper(*args, **kwargs):
            definition = "[@F #ed8796]def"
            name = f"[@F #8aadf4]{TED.encode(obj.__name__)}[@F]"
            sig = f"{parse_signature(obj)}"

            logger.custom(
                label=f"{TED.encode(obj.__qualname__)} [@F green]🡆",
                clr="yellow",
            )

            logger.message("\n" + TED.parse(f"  {definition} {name}{sig}"))

            logger.message(
                f"""  args: {p_value([
                        arg for arg in args
                        if not (isinstance(arg, Callable)
                        and arg.__name__ != obj.__qualname__.split('.')[0])
                    ], depth=depth, indent=4)}\n""",
            )

            for key, value in kwargs.items():
                logger.message(f"  {key}={p_value(value, depth=depth, indent=4)}\n")

            result = obj(*args, **kwargs)
            logger.message(
                TED.parse(
                    f"  *returns*: {p_value(result, decode=False, depth=depth, indent=4)}\n"
                ),
            )
            logger.custom(
                label=f"[@F red]🡄[@F yellow]{TED.encode(obj.__qualname__)}",
                clr="yellow",
            )
            logger.flush()
            input()

        return debug_wrapper

    return decorator
