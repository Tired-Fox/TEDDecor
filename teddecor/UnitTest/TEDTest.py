from __future__ import annotations
import ast
import argparse
import os

from ..UnitTest import TestSuite, SaveType
from ..Util import slash


def get_test_functions(module: ast.Module) -> list:
    """Retrieve the test case names from the given module.

    Args:
        module (ast.Module): The module to parse test cases from.

    Returns:
        list: Test case names
    """
    return [
        obj.name
        for obj in module.body
        if isinstance(obj, ast.FunctionDef)
        and "test" in [decor.id for decor in obj.decorator_list]
    ]


def get_test_classes(module: ast.Module) -> list:
    """Retrieve the test class names from the given module.

    Args:
        module (ast.Module): The module the parse classes from.

    Returns:
        list: Test class names.
    """
    return [
        obj.name
        for obj in module.body
        if isinstance(obj, ast.ClassDef) and "Test" in [base.id for base in obj.bases]
    ]


def get_files(dir: str) -> list[str]:
    """Gets the python files/modules from the specified directory

    Args:
        dir (str): The directory to recursively search

    Returns:
        list[str]: The python files found in the specified directory
    """

    os.chdir(dir)
    from glob import glob

    return [y for x in os.walk(f".{slash()}") for y in glob(os.path.join(x[0], "*.py"))]


def generate_suite(files: list[str], name: str) -> TestSuite:
    """Generates a TestSuite with the tests pulled from the found modules.

    Args:
        files (list[str]): The files/modules that have tests.
        name (str): The name of the test suite.

    Returns:
        TestSuite: The TestSuite with all tests added to it.
    """

    test_suite = TestSuite(name=name)
    curdir = os.getcwd()

    for file in files:
        mdir = file.split(slash())[0]
        mname = file.split(slash())[-1].split(".")[0]

        with open(file, "r", encoding="utf-8") as fd:
            file_content = fd.read()

        module = ast.parse(file_content)
        runners = get_test_classes(module) + get_test_functions(module)

        os.chdir(mdir)
        try:
            # Bring module into scope and grab it
            path.insert(0, "./")
            mod = __import__(mname)

            # For each of the valid test objects add them to the test suite
            for runner in runners:
                if hasattr(mod, runner):
                    test_suite.append(getattr(mod, runner))

        except Exception as error:
            # TODO: Properly look at errors and display them
            # Don't stop as it could be module level errors that cause the code to go to this block
            print(error)

        os.chdir(curdir)

    return test_suite


def get_args() -> dict:
    """Parse the passed in arguments with `ArgParse`

    Raises:
        Exception: If the user specifies a start directory and it does not exist.

    Returns:
        dict: The key value pairs of the arguments passed in.
    """
    from os import getcwd

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-n",
        "--name",
        help="The name of the group of tests that will be run.\nShows up as the test suite name.",
    )
    parser.add_argument(
        "-e",
        "--entry",
        help="The entry point where the scan for tests will start.",
    )
    parser.add_argument(
        "-s",
        "--save",
        help="The file type that the results will be saved too.",
    )
    parser.add_argument(
        "-r",
        "--regex",
        help="Regex to apply so only matching tests are run.",
    )
    parser.add_argument(
        "-o",
        "--save_path",
        help="Relative path on where to save the results.",
    )

    args = parser.parse_args()
    variables = {
        "path": None,
        "save": None,
        "regex": None,
        "save_path": "",
        "name": None,
    }

    if args.entry is None:
        variables["path"] = str(getcwd())
    else:
        from re import split

        if args.entry.startswith("~"):
            from pathlib import Path

            args.entry = str(Path.home()) + args.entry[1:]

        if os.path.isdir(args.entry):
            variables["path"] = slash().join(split(r"[\\/]", args.entry))
        else:
            raise Exception(f"{dir} is not a directory")

    if args.save is not None and args.save.lower() in ["json", "csv", "txt", "all"]:
        if args.save == "all":
            variables["save"] = SaveType.ALL()
        else:
            variables["save"] = f".{args.save.lower()}"

    if args.regex is not None:
        variables["regex"] = args.regex

    if args.save_path is not None:
        variables["save_path"] = args.save_path

    if args.name is not None:
        variables["name"] = args.name
    else:
        variables["name"] = variables["path"].split(slash())[-1]

    return variables


def main():
    # TODO: display type

    arguments = get_args()

    files = get_files(arguments["path"])
    suite = generate_suite(files, arguments)
    if len(suite.tests) > 0:
        results = suite.run(regex=arguments["regex"])
        if arguments["save"] is not None:
            results.save(location=arguments["save_path"], ext=arguments["save"])


if __name__ == "__main__":
    main()