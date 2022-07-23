def __slash() -> str:
    from sys import platform

    if "win" in platform:
        return "\\"
    
    return "/"


def import_scope(rel_path: str = "../"):
    path = rel_path.replace('\\/', __slash())
    
    if path[0] == "~":
        from pathlib import Path
        path = path.replace('~', str(Path.home()))

    import sys
    sys.path.insert(0, path)
