"""Testing

This module contains the base class and decorator for running tests.
In a sense, this module is the brains of teddecor's unit testing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Pattern, Union

from ..Util import *

__all__ = ["test", "Test", "runTest", "TestResult", "ResultType"]


def runTest(test: Callable) -> TestResult:
    """Runs a function decorated with `@test` and constructs it's results.

    Args:
        test (Callable): @test function to run

    Returns:
        dict: Formated results from running the test

    Raises:
        TypeError: When the callable test is not decorated with `@test`
    """

    if test.__name__ == "test_wrapper":
        _result = TestResult(test())
        return _result
    else:
        raise TypeError("Test function must have @test decorator")


def __getTracback(error: Exception) -> list:
    """Generate a fromatted traceback from an error.

    Args:
        error (Exception): Raised exception to extract the traceback from

    Returns:
        list: The formatted traceback
    """
    import traceback

    stack = []
    for frame in traceback.extract_tb(error.__traceback__):
        if "test_wrapper" not in frame.name:
            stack.append(
                f"[{frame.filename.split(slash())[-1]}:{frame.lineno}] {frame.name}"
            )

    if str(error) == "":
        if isinstance(error, AssertionError):
            message = "Assertion Failed"
        else:
            message = f"Unkown exception <{error.__class__.__name__}>"
    else:
        message = str(error)

    stack.append(f"[Error Message] {message}")

    return stack


def test(func):
    """Decorator for test case (function)."""

    def test_wrapper(*args, **kwargs):
        """Executes the function this decorator is on and collect the run results.

        Returns:
            tuple: The test run results. Formatted in the order of function name, type of result, and addition info.

        Note:
            In the case of a skip and failed result the info portion is filled it with the type of skip and the traceback respectivily.
        """
        try:
            func(*args, **kwargs)
        except AssertionError as error:
            return (func.__name__, ResultType.FAILED, __getTracback(error))
        except NotImplementedError:
            return (func.__name__, ResultType.SKIPPED, "Not Implemented")

        return (func.__name__, ResultType.SUCCESS, "")

    return test_wrapper


@dataclass
class ResultType:
    """Enum/Dataclass that describes the test run result.

    Attributes:
        SUCCESS (tuple[str, str]): Message and color for a successful test run
        FAILED (tuple[str, str]): Message and color for a failed test run
        SKIPPED (tuple[str, str]): Message and color for a skipped test run
    """

    SUCCESS: tuple[str, str] = ("Passed", "\x1b[1;32m")
    FAILED: tuple[str, str] = ("Failed", "\x1b[1;31m")
    SKIPPED: tuple[str, str] = ("Skipped", "\x1b[1;33m")


class TestResult:
    def __init__(self, result: tuple[str, ResultType, Union[str, list]] = None):
        if result is not None:
            self._name = result[0]
            self._result = result[1]
            self._info = result[2]
        else:
            self._name = "Unknown"
            self._result = ResultType.SKIPPED
            self._info = "Unkown test"

    @property
    def fname(self) -> str:
        return self._name

    @property
    def result(self) -> str:
        return self._result[0]

    @property
    def color(self) -> str:
        return self._result[1]

    @property
    def info(self) -> Union[str, list]:
        return self._info

    def str(self, indent: int = 0) -> str:
        """Used to convert result into a string. Allows for additional indentationto be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            str: The formatted result as a string with indent

        Note:
            If you don't plan to add additional indent use the implement __str__ method.
            str(TestResult) or print(TestResult).
        """
        out = " " * indent
        out += f"{self.fname} (Case) ... {self.color}{self.result}\x1b[0m"
        if isinstance(self.info, list):
            for trace in self.info:
                out += "\n" + " " * (indent + 4) + trace
        else:
            out += self.info

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """
        return {self.fname: {"result": self._result, "info": self.info}}

    def __str__(self):
        out = f"{self.fname} (Case) ... {self.color}{self.result}\x1b[0m"
        if isinstance(self.info, list):
            for trace in self.info:
                out += "\n" + trace
        else:
            out += self.info

        return out


class Test:
    """Class used to indentify and run tests. It will also print the results to the screen."""

    def __init__(self):
        self._results = []

    @property
    def results(self) -> dict:
        """List of test results"""
        return self._results

    @results.setter
    def results(self, new_results: dict):
        """Set list of test results"""
        self._results = new_results

    def getCount(self) -> tuple:
        """Count the number of passed, failed, and unimplemented tests.

        Returns:
            int: Total failed tests
        """

        totals = [0, 0, 0]
        for test_result in self.results:
            if test_result.result == ResultType.SUCCESS[0]:
                totals[0] += 1
            elif test_result.result == ResultType.FAILED[0]:
                totals[1] += 1
            elif test_result.result == ResultType.SKIPPED[0]:
                totals[2] += 1
        return tuple(totals)

    def getNodeValue(self, node) -> bool:
        """Gets the decorator value from node

        Args:
            node (Any): Any ast node type

        Returns:
            str: id of ast.Name node
        """
        import ast

        if isinstance(node, ast.Attribute):  # and node.attr in valid_paths:
            if "test" in node.attr:
                return True

        elif isinstance(node, ast.Name):
            if "test" in node.id:
                return True

        return False

    def getTests(self, regex: Pattern) -> list:
        """Gets all function names in the current class decorated with `@test`self.

        Returns:
            list: Function names decorated with `@test`
        """
        import ast
        import inspect

        result = []

        def visit_FunctionDef(node):
            """Checks given ast.FunctionDef node for a decorator `test` and adds it to the result."""
            import re

            for decorator in node.decorator_list:
                if self.getNodeValue(decorator):
                    if regex is not None and re.match(regex, node.name):
                        result.append(node.name)
                    elif regex is None:
                        result.append(node.name)
                else:
                    continue

        visitor = ast.NodeVisitor()
        visitor.visit_FunctionDef = visit_FunctionDef
        visitor.visit(
            compile(inspect.getsource(self.__class__), "?", "exec", ast.PyCF_ONLY_AST)
        )

        return result

    def executeTests(self, regex: Pattern, display: bool = True) -> None:
        """Will execute all functions decorated with `@test`"""

        fnames: list = self.getTests(regex)
        """Function names decorated with `@test`"""

        klass = self.__class__.__name__

        for name in fnames:
            result = runTest(getattr(self, name))
            self.results.append(result)

        if display:
            print(self.str(tests=False))

    def dict(self) -> dict:
        """Converts the test classes results into a dictionary

        Returns:
            dict: Results organized by test case (function)

        Note:
            The dictionary will have a single key which is the class name that is another dictionary. Inside that dictionary is where the totals for passed, skipped, and failed are stored in a tuple respectivily.
            This is also where the result and information for each test case.
        """
        klass = self.__class__.__name__
        totals = self.getCount()
        out = {f"{klass}": {"totals": totals}}

        for result in self.results:
            out[klass].update(result.dict())

        return out

    def str(self, indent: int = 0, case_results: bool = True) -> str:
        klass = self.__class__.__name__
        passed, failed, skipped = self.getCount()

        totals = f"\x1b[1m[{ResultType.SUCCESS[1]}{passed}\x1b[37m:{ResultType.SKIPPED[1]}{skipped}\x1b[37m\
:{ResultType.FAILED[1]}{failed}\x1b[37m]\x1b[0m"

        out = " " * indent + f"\x1b[1m{klass} (Class)\x1b[0m " + totals

        if case_results:
            if len(self.results) > 0:
                for test_result in self.results:
                    out += "\n" + test_result.str(indent=(4 + indent))
            else:
                out += (
                    " " * (indent + 4)
                    + f"\x1b[1;33mNo Tests Found for {self.__class__.__name__}\x1b[0m"
                )

        return out

    def run(self, display: bool = True, regex: Pattern = None) -> Test:
        """Will find and execute all tests in class. Prints results when done."""

        self.executeTests(regex=regex, display=display)
        return self
