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
            return (func.__name__, "Failed", __get_tracback(error))

        return (func.__name__, "Passed", "")

    return wrapper


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
                if isinstance(result[2], list):
                    stack = "\n     ".join(result[2])
                else:
                    stack = ""

                if result[1] == "Passed":
                    success = f"\x1b[1;32m{result[1]}\x1b[0m"
                else:
                    success = f"\x1b[1;31m{result[1]}\x1b[0m"
                    
                print(
                    "   ",
                    result[0],
                    "...",
                    success,
                    f"\n     {stack}",
                )
            print(
                f"\n\x1b[1mTotal\x1b[0m: {len(self.results)} \
\x1b[1;32mPassed\x1b[0m: {len(self.results) - failed} \
\x1b[1;31mFailed\x1b[0m: {failed}"
            )
        else:
            print(f"    \x1b[1;33mNo Tests Found for {self.__class__.__name__}\x1b[0m")

    
    def asdict(self) -> dict:
        out = { f"{self.__class__.__name__}" : {}}

        for result in self.results:
            out[self.__class__.__name__][result[0]] = { "result": result[1], "stack": result[2]}

        return out

    def main(self, display: bool = True) -> dict:
        """Will find and execute all tests in class. Prints results when done."""

        self.execute_tests()

        if display:
            self.print_results()

        return self.asdict()
