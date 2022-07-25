"""Util

A collection of modules and helpful features that that are commonly used.
"""

__all__ = ["import_scope", "slash"]


def slash() -> str:
    """Get the type of slash based on the os.

    Returns:
        str: OS filesystem specific slash character
    """
    from sys import platform

    return "\\" if "win" in platform else "/"


def import_scope(rel_path: str = "../"):
    """Imports a directory to your pythons env path. This allows you to use a module or package that is in a local directory but out of scope."""
    path = rel_path.replace("\\/", slash())

    if path.startswith("~"):
        from pathlib import Path

        path = path.replace("~", str(Path.home()))

    from sys import path as envpath

    envpath.insert(0, path)
