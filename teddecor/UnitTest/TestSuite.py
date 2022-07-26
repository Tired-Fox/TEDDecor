"""Test Suite

A collection of tests that are to be run.
Can be either test classes or individual test cases.
"""
from inspect import isclass
from typing import Pattern, Union
from .Testing import ResultType, Test, TestResult, test, runTest

__all__ = ["TestSuite"]

# TODO: Change manual formatting to TED formatter
# PERF: Add Graph SVG output
# PERF: Add CSV Output
class TestSuite:
    """Run the given test classes or filter with regex."""

    def __init__(
        self,
        name: str,
        tests: list[Union[Test, test]] = None,
        regex: Pattern = None,
    ):
        """Start with a list of Test classes or test functions. The function name patter can also be specified.
            Lastly you can specify whether a Test class outputs the result

        Args:
            tests (list[Union[Test, test]], optional): _description_. Defaults to None.
            regex (Pattern, optional): _description_. Defaults to None.
            output (bool, optional): _description_. Defaults to True.
        """
        self._name = name
        self._tests = tests
        self._regex = regex
        self._results = {name: []}

    @property
    def name(self) -> str:
        return self._name

    @property
    def tests(self) -> Union[list, None]:
        return self._tests

    @tests.setter
    def tests(self, tests: list[Test]):
        self._tests = tests

    @property
    def regex(self) -> Union[str, None]:
        return self._regex

    @regex.setter
    def regex(self, regex: str):
        self._regex = regex

    @property
    def results(self) -> Union[dict, None]:
        return self._results

    def run(
        self,
        display: bool = True,
        class_results: bool = True,
        case_results: bool = True,
    ) -> dict:
        """Run all the provided test classes and cases.q

        Args:
            display (bool, optional): Whether to display anything. Defaults to True.
            class_results (bool, optional): Whether to show individul class results. Defaults to True.
            case_results (bool, optional): Whether to show individual case results. Defaults to True.

        Returns:
            dict: Dictionary of results
        """

        self._results[self.name] = []

        for test in self.tests:
            if isclass(test):
                self._results[self.name].append(
                    test().run(regex=self.regex, display=False)
                )
            else:
                self._results[self.name].append(runTest(test))

        self.prettify(display, class_results, case_results)

        return self.results

    def prettify(
        self, display: bool, class_results: bool = True, case_results: bool = True
    ):
        """Will print the results of the classes and cases in a formatted way

        Args:
            display (bool, optional): Whether to display anything. Defaults to True.
            class_results (bool, optional): Whether to show individul class results. Defaults to True.
            case_results (bool, optional): Whether to show individual case results. Defaults to True.
        """

        if display:
            passed, failed, skipped = self.getCount()

            totals = f"\x1b[1m[{ResultType.SUCCESS[1]}{passed}\x1b[37m:{ResultType.SKIPPED[1]}{skipped}\x1b[37m\
:{ResultType.FAILED[1]}{failed}\x1b[37m]\x1b[0m"

            print(f"\x1b[1m{self.name} (Suite)\x1b[0m", totals)

            for result in self.results[self.name]:
                if case_results and isinstance(result, TestResult):
                    print(result.write(indent=4))
                elif class_results:
                    print(result.str(indent=4))

    def getCount(self) -> tuple:
        """Count the number of passed, failed, and skipped tests respectively

        Returns:
            tuple: The amount of passed, failed, and skipped tests
        """
        totals = [0, 0, 0]

        for result in self.results[self.name]:
            passed, failed, skipped = result.getCounts()
            totals[0] += passed
            totals[1] += failed
            totals[2] += skipped

        return tuple(totals)
