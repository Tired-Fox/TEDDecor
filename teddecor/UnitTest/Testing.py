"""Testing

This module contains the base class and decorator for running tests.
In a sense, this module is the brains of teddecor's unit testing.
"""
from __future__ import annotations

from typing import Callable, Pattern

from .Results import TestResult, ClassResult, ResultType
from ..Util import *

__all__ = ["test", "Test", "run", "TestResult", "wrap"]


def run(test: Callable, display: bool = True) -> TestResult:
    """Runs a single test case, function decorated with `@test` and constructs it's results.

    Args:
        test (Callable): @test function to run

    Returns:
        dict: Formated results from running the test

    Raises:
        TypeError: When the callable test is not decorated with `@test`
    """

    if test.__name__ == "test_wrapper":
        _result = TestResult(test())
        if display:
            _result.write()
        return _result
    else:
        raise TypeError("Test function must have @test decorator")


def wrap(func: Callable, *args, **kwargs) -> Callable:
    """Used to return a lambda that runs the function with the given args.
    This is so that the function can be run later with provided parameters

    Args:
        func (Callable): Function to run

    Returns:
        Callable: Lambda of the funciton to be run later
    """
    return lambda: func(*args, **kwargs)


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
            return (func.__name__, ResultType.SKIPPED, "")

        return (func.__name__, ResultType.SUCCESS, "")

    return test_wrapper


class Test:
    """Class used to indentify and run tests. It will also print the results to the screen."""

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

    def executeTests(self, regex: Pattern) -> ClassResult:
        """Will execute all functions decorated with `@test`"""

        fnames: list = self.getTests(regex)
        """Function names decorated with `@test`"""

        results = ClassResult(name=self.__class__.__name__)

        for name in fnames:
            results.append(run(getattr(self, name), display=False))

        return results

    def run(self, display: bool = True, regex: Pattern = None) -> ClassResult:

        """Will find and execute all tests in class. Prints results when done.

        Args:
            display (bool, optional): Whether to display the results
            regex (Pattern, optional): Pattern of which tests should be run

        Returns:
            ClassResult: Results object that can save and print the results
        """

        results = self.executeTests(regex=regex)

        if display:
            results.write()

        return results
