from dataclasses import dataclass

__all__ = [
    "test",
    "Test"
]


def __slash() -> str:
    from platform import platform
    return "\\" if "win" in platform() else "/" 


def __get_tracback(error: Exception) -> list:
    """Generate a fromatted traceback from an error.

    Args:
        error (Exception): Raised exception to extract the traceback from

    Returns:
        list: The formatted traceback
    """
    import traceback

    stack = []
    for frame in (traceback.extract_tb(error.__traceback__)):
        if "wrapper" not in frame.name:
            stack.append(f"[{frame.filename.split(__slash())[-1]}:{frame.lineno}] {frame.name}")

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
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AssertionError as error:
            return (func.__name__, TestResult.FAILED, __get_tracback(error))
        except NotImplementedError:
            return (func.__name__, TestResult.SKIPPED, "Not Implemented")

        return (func.__name__, TestResult.SUCCESS, "")

    return wrapper

@dataclass
class TestResult():
    SUCCESS: tuple[str, str] = ("Passed", "\x1b[1;32m")
    FAILED: tuple[str, str] = ("Failed", "\x1b[1;31m")
    SKIPPED: tuple[str, str] = ("Skipped", "\x1b[1;33m")


class Test():
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

    def get_count(self) -> tuple:
        """Count the number of passed, failed, and unimplemented.

        Returns:
            int: Total failed tests
        """
        totals = [0, 0, 0]
        for result in self.results:
            if result[1] == TestResult.SUCCESS:
                totals[0] += 1
            elif result[1] == TestResult.FAILED:
                totals[1] += 1
            elif result[1] == TestResult.SKIPPED:
                totals[2] += 1
        return tuple(totals)

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

        passed, failed, skipped = self.get_count()
        totals = f"\x1b[1m[{TestResult.SUCCESS[1]}{passed}\x1b[37m:{TestResult.SKIPPED[1]}{skipped}\x1b[37m:{TestResult.FAILED[1]}{failed}\x1b[37m]\x1b[0m" 
        print(f"\x1b[1m{self.__class__.__name__}\x1b[0m", totals)
        if len(self.results) > 0:


            for result in self.results:
                if isinstance(result[2], list): 
                    stack = "\n     " + "\n     ".join(result[2])
                elif result[2] != "":
                    stack = "\n        " + result[2]
                else:
                    stack = result[2]

                success = f"{result[1][1]}{result[1][0]}\x1b[0m"
                    
                print(
                    "   ",
                    result[0],
                    "...",
                    success,
                    stack,
                )
#             print(
#                 f"\n\x1b[1mTotal\x1b[22m: {len(self.results)} \
# {TestResult.SUCCESS[1]}{TestResult.SUCCESS[0]}\x1b[0m: {passed} \
# {TestResult.FAILED[1]}{TestResult.FAILED[0]}\x1b[0m: {failed} \
# {TestResult.SKIPPED[1]}{TestResult.SKIPPED[0]}\x1b[0m: {skipped}"
#             )
        else:
            print(f"    \x1b[1;33mNo Tests Found for {self.__class__.__name__}\x1b[0m")

    
    def asdict(self) -> dict:
        totals = self.get_count()
        out = { f"{self.__class__.__name__}" : { "totals": totals } }

        for result in self.results:
            out[self.__class__.__name__].update({ result[0]: { "result": result[1][0], "info": result[2]} })

        return out

    def main(self, display: bool = True) -> dict:
        """Will find and execute all tests in class. Prints results when done."""

        self.execute_tests()

        if display:
            self.print_results()

        return self.asdict()
