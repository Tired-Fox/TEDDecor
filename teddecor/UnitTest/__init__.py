from .asserts import *


def test(func):
    # TODO: Make test return a generator will all errors
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as error:
            return (func.__name__, "\x1b[1;31mFailed\x1b[0m", error)

        return (func.__name__, "\x1b[1;32mPassed\x1b[0m", "")

    return wrapper

from typing import Callable

class UnitTest():
    """Class used to indentify and run test results. It will also print the results to the screen."""

    def __init__(self):
        self._results = []

    @property
    def results(self) -> list:
        """List of test results"""
        return self._results

    @results.setter
    def results(self, new_results: list):
        """Set list of test results"""
        self._results = new_results

    def get_failed(self) -> int:
        """Count the number of failed test funcitonsself.

        Returns:
            int: Total failed tests
        """
        total = 0
        for result in self.results:
            if "Failed" in result[1]:
                total += 1
        return total

    def get_node_val(self, node) -> bool:
        """Gets the decorator value from node

        Args:
            node (Any): Any ast node type

        Returns:
            str: id of ast.Name node
        """
        import ast
        
        if isinstance(node, ast.Attribute):# and node.attr in valid_paths:
            if "test" in node.attr:
                return True

        elif isinstance(node, ast.Name):
            if "test" in node.id:
                return True
         
        return False

    def get_tests(self) -> list:
        """Gets all function names in the current class decorated with `@test`self.

        Returns:
            list: Function names decorated with `@test`
        """
        import ast
        import inspect

        result = []

        def visit_FunctionDef(node):
            """Checks given ast.FunctionDef node for a decorator `test` and adds it to the result."""
            valid_paths = ['teddecor', 'UnitTest']
            for decorator in node.decorator_list:
                if self.get_node_val(decorator):
                    result.append(node.name)
                else:
                    continue

        visitor = ast.NodeVisitor()
        visitor.visit_FunctionDef = visit_FunctionDef
        visitor.visit(
            compile(inspect.getsource(self.__class__), "?", "exec", ast.PyCF_ONLY_AST)
        )

        return result

    def execute_tests(self) -> None:
        """Will execute all functions decorated with `@test`"""

        fnames: list = self.get_tests()
        """Function names decorated with `@test`"""

        for name in fnames:
            func = getattr(self, name)
            self.results.append(func())

    def print_results(self) -> None:
        """Formats and prints the results"""

        print(f"\x1b[1m{self.__class__.__name__}\x1b[0m", ":\n")
        if len(self.results) > 0:
            failed: int = self.get_failed()

            for result in self.results:
                print(
                    "   ",
                    result[0],
                    "...",
                    result[1],
                    f"\n        {result[2]}" if result[2] else "",
                )
            print(
                f"\n\x1b[1mTotal\x1b[0m: {len(self.results)} \
\x1b[1;32mPassed\x1b[0m: {len(self.results) - failed} \
\x1b[1;31mFailed\x1b[0m: {failed}"
            )
        else:
            print(f"    \x1b[1;33mNo Tests Found for {self.__class__.__name__}\x1b[0m")

    # TODO: Make main return the results in a standard way 
    def main(self) -> None:
        """Will find and execute all tests in class. Prints results when done."""

        self.execute_tests()
        self.print_results()