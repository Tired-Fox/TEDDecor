"""Util

A collection of modules and helpful features that that are commonly used.
"""


def __slash() -> str:
    """Get the operating system specific slash character for the filesystem.

    Returns:
        str: The oppropriate slash character
    """
    from sys import platform

    if "win" in platform:
        return "\\"
    
    return "/"


def import_scope(rel_path: str = "../"):
    """Imports a directory to your pythons env path. This allows you to use a module or package that is in a local directory but out of scope."""
    path = rel_path.replace('\\/', __slash())
    
    if path[0] == "~":
        from pathlib import Path
        path = path.replace('~', str(Path.home()))

    import sys
    sys.path.insert(0, path)
