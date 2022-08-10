"""Results

TestResults, ClassResults, and SuiteResults all hold and translate the test result information
into a structure that is easy to use and has mutliple outputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from ..Util import slash
from ..TED.markup import TED
from .Objects import TestFilter

__all__ = [
    "TestResult",
    "ClassResult",
    "SuiteResult",
    "SaveType",
    "ResultTypes",
    "RunResults",
]


class Count:
    def __init__(self, result: ResultType = None):
        if result == ResultTypes.PASSED:
            self._count = [1, 0, 0]
        elif result == ResultTypes.FAILED:
            self._count = [0, 1, 0]
        elif result == ResultTypes.SKIPPED:
            self._count = [0, 0, 1]
        else:
            self._count = [0, 0, 0]

    @property
    def total(self) -> list[int, int, int]:
        return self._count

    def __add__(self, obj: Count) -> Count:
        if isinstance(obj, Count):
            for i in range(len(self._count)):
                self._count[i] += obj.total[i]
            return self
        else:
            raise TypeError(f"Invalid type {type(obj)}")

    def __iadd__(self, obj: Count) -> Count:
        if isinstance(obj, Count):
            for i in range(len(self._count)):
                self._count[i] += obj.total[i]
            return self
        else:
            raise TypeError(f"Invalid type {type(obj)}")


class ResultType:
    def __init__(
        self,
        name: str,
        symbol: str,
        color: str,
        filter: list[TestFilter] = [TestFilter.OVERALL],
    ):
        self._color = color
        self._symbol = symbol
        self._name = name
        self._filter = filter

    @property
    def color(self) -> str:
        """Color of the result."""
        return self._color

    @property
    def symbol(self) -> str:
        """Results associated symbol."""
        return self._symbol

    @property
    def name(self) -> str:
        """Results name."""
        return self._name

    @property
    def filter(self) -> str:
        """Results filter."""
        return self._filter

    def __eq__(self, obj: ResultType) -> bool:
        if not isinstance(obj, type(self)):
            return False

        return (
            self.color == obj.color
            and self.symbol == obj.symbol
            and self.color == obj.color
            and self.name == obj.name
            and self.filter == obj.filter
        )

    def __str__(self) -> str:
        return self.color + self.symbol

    def __repr__(self) -> str:
        return f"""{self.name} (
  symbol: {self.symbol},
  color: {self.color},
  filter: {self.filter}
)"""


@dataclass
class ResultTypes:
    """Enum/Dataclass that describes the test run result.

    Attributes:
        SUCCESS (tuple[str, str]): Message and color for a successful test run
        FAILED (tuple[str, str]): Message and color for a failed test run
        SKIPPED (tuple[str, str]): Message and color for a skipped test run
    """

    PASSED: ResultType = ResultType("Passed", "✓", "[@F green]", TestFilter.PASSED)
    FAILED: ResultType = ResultType("Failed", "x", "[@F red]", TestFilter.FAILED)
    SKIPPED: ResultType = ResultType("Skipped", "↻", "[@F yellow]", TestFilter.SKIPPED)


@dataclass
class SaveType:
    """Enum/Dataclass that describes the save file extension/type.

    Attributes:
        CSV (str): `.csv` Save results as a CSV file
        JSON (str): `.json` Save results as a JSON file
        TXT (str):  `.txt` Save results as a TXT file
    """

    CSV: str = ".csv"
    JSON: str = ".json"
    TXT: str = ".txt"
    ALL: callable = lambda: [".txt", ".json", ".csv"]


class Result:
    """Base class for result types"""

    def __init__(self):
        self._counts = Count()

    @property
    def count(self) -> Count:
        """Get counts for passed, failed, skipped.

        Returns:
            tuple: The values for passed, failed, skipped respectively
        """
        return self._counts

    @property
    def name(self) -> str:
        return self._name

    def write(self, filter: TestFilter, indent: int = 0):
        """Output the result(s) to the screen

        Args:
            indent (int, optional): The amount to indent the values. Defaults to 0.
        """
        for line in self.pretty(filter, indent):
            TED.print(line)

    def pretty(self, filter: TestFilter, indent: int) -> list:
        """Format the result(s) into a formatted list

        Returns:
            list: List of formatted result(s)
        """
        return []

    def dict(self) -> dict:
        """Generate the dictionary varient of the results

        Returns:
            dict: The results formatted as a dictionary
        """
        return {}

    def isdir(self, location: str) -> Union[str, None]:
        """Takes the location that the file is to be saved then changes directory.

        Args:
            location (str, optional): The location where the file will be saved. Defaults to None.

        Returns:
            str, None: The absolute path or None if path doesn't exist

        Note:
            This is to be used with an inherited class and will auto convert `~` to it's absolute path
        """

        if location != "":
            from os import path

            if location.startswith("~"):
                from pathlib import Path

                location = str(Path.home()) + location[1:]

            if not path.isdir(location):
                return None

            if not location.endswith(slash()):
                location += slash()

        return location

    def __str__(self):
        return "\n".join(self.pretty())

    def __repr__(self):
        return "\n".join(self.str())


class TestResult(Result):
    def __init__(self, result: tuple[str, ResultTypes, Union[str, list]] = None):
        super().__init__()

        if result is not None:
            self._name = result[0]
            self._result = result[1]
            self._info = result[2]
        else:
            self._name = "Unknown"
            self._result = ResultTypes.SKIPPED
            self._info = "Unkown test"

        self._counts = Count(self._result)

    @property
    def result(self) -> str:
        return self._result

    @property
    def filter(self) -> str:
        return self._result.filter

    @property
    def color(self) -> str:
        return self._result.color

    @property
    def symbol(self) -> str:
        return self._result.symbol

    @property
    def info(self) -> Union[str, list]:
        return self._info

    def pretty(
        self, filter: list[TestFilter] = [TestFilter.NONE], indent: int = 0
    ) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """
        out = []
        if TestFilter.NONE not in filter:
            if TestFilter.OVERALL in filter or self.result.filter in filter:
                out.append(
                    "".ljust(indent, " ")
                    + f"\[{self.color}{self.symbol}[@F]] {TED.encode(self.name)}"
                )
                if isinstance(self.info, list):
                    for trace in self.info:
                        out.append("".ljust(indent + 4, " ") + trace)
                else:
                    if self.info != "":
                        out.append("".ljust(indent + 4, " ") + self.info)

        return out

    def str(self, indent: int = 0) -> list:
        """Results formatted into lines without colors

        Args:
            indent (int, optional): The amount to indent the lines. Defaults to 0.

        Returns:
            list: The results as lines
        """
        out = []
        out.append(" " * indent + f"[{self.symbol}] {self.name}")
        if isinstance(self.info, list):
            for trace in self.info:
                out.append(" " * (indent + 4) + TED.strip(trace))
        else:
            if self.info != "":
                out.append(" " * (indent + 4) + self.info)

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """
        info = (
            [TED.strip(elem) for elem in self.info]
            if isinstance(self.info, list)
            else [TED.strip(self.info)]
        )
        return {self.name: {"result": self._result.name, "info": info, "type": "Case"}}

    def csv(self) -> str:
        """The results formatted as CSV

        Returns:
            str: CSV format of the result
        """
        info = (
            "\n".join(TED.strip(elem) for elem in self.info)
            if isinstance(self.info, list)
            else TED.strip(self.info)
        )
        return f'{self.name},{self.result},"{info}"'

    def save(
        self, location: str = "", ext: Union[str, list[str]] = SaveType.CSV
    ) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """

        location = self.isdir(location)

        if isinstance(ext, str):
            self.__save_to_file(location, ext)
        elif isinstance(ext, list):
            for ext in ext:
                self.__save_to_file(location, ext)
        return True

    def __save_to_file(self, location: str, type: str) -> bool:
        """Saves the data to a given file type in a given location

        Args:
            location (str): Where to save the file
            type (str): Type of file to save, CSV, JSON, TXT

        Returns:
            bool: True if file was saved
        """
        if location is not None:
            with open(location + self.name + type, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Case,result,info\n")
                    file.write(self.csv())
                    return True
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                    return True
                elif type == SaveType.TXT:
                    file.write(repr(self))
                    return True
        else:
            return False


class ClassResult(Result):
    def __init__(self, name: str, results: list[TestResult] = None):
        super().__init__()

        self._results = []
        if results is not None:
            for result in results:
                self.append(result)

        self._name = name

    @property
    def results(self) -> list:
        return self._results

    def append(self, result: TestResult):
        """Add a result to the list of results. This will also increment the counts.

        Args:
            result (Union[TestResult, ClassResult]): The result to add to the colleciton of results
        """
        self._counts += result.count
        self._results.append(result)

    def pretty(self, filter: list[TestFilter], indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []

        if TestFilter.NONE not in filter:
            if TestFilter.OVERALL in filter or TestFilter.TOTALS in filter:
                passed, failed, skipped = self.count.total
                totals = f"\[{ResultTypes.PASSED.color}{passed}[@F]:{ResultTypes.SKIPPED.color}{skipped}[@F]\
:{ResultTypes.FAILED.color}{failed}[@F]]"
                out.append(" " * indent + f"*{totals} {TED.encode(self.name)}")

            if TestFilter.OVERALL not in filter:
                if len(self.results) > 0:
                    for result in self.results:
                        if result.filter in filter:
                            out.extend(result.pretty(indent=indent + 4))
                else:
                    out.append(
                        " " * (indent + 4)
                        + f"[@F yellow]No Tests Found for {TED.encode(self.name)}"
                    )

        return out

    def str(self, indent: int = 0) -> list:
        """Results formatted into lines without colors

        Args:
            indent (int, optional): The amount to indent the lines. Defaults to 0.

        Returns:
            list: The results as lines
        """
        out = []

        passed, failed, skipped = self.count.total
        out.append(" " * indent + f"[C:{passed}:{skipped}:{failed}] {self.name}")

        if len(self.results):
            for result in self.results:
                out.extend(result.str(indent + 4))
        else:
            out.append(" " * (indent + 4) + f"No Tests Found for {self.name}")

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """

        out = {self.name: {"type": "Class", "results": []}}

        for result in self.results:
            out[self.name]["results"].append(result.dict())

        return out

    def csv(self) -> list:
        """The test case results. Each index is a different line in the file

        Returns:
            list: The lines to be written to a CSV file
        """

        out = []

        for result in self.results:
            out.append(f"{self.name}," + result.csv())

        return out

    def save(
        self, location: str = "", ext: Union[str, list[str]] = SaveType.CSV
    ) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """

        location = self.isdir(location)

        if isinstance(ext, str):
            self.__save_to_file(location, ext)
        elif isinstance(ext, list):
            for ext in ext:
                self.__save_to_file(location, ext)
        return True

    def __save_to_file(self, location: str, type: str) -> bool:
        """Saves the data to a given file type in a given location

        Args:
            location (str): Where to save the file
            type (str): Type of file to save, CSV, JSON, TXT

        Returns:
            bool: True if file was saved
        """
        if location is not None:
            with open(location + self.name + type, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Class,Test Case,Result,Info\n")
                    for line in self.csv():
                        file.write(f"{line}\n")
                    return True
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                    return True
                elif type == SaveType.TXT:
                    file.write(repr(self))
                    return True
        else:
            return False


class SuiteResult(Result):
    def __init__(self, name: str):
        super().__init__()

        self._name = name
        self._results = []

    @property
    def results(self) -> list:
        return self._results

    def append(self, result: Union[TestResult, ClassResult]):
        """Add a result to the list of results. This will also increment the counts.

        Args:
            result (Union[TestResult, ClassResult]): The result to add to the colleciton of results
        """
        self._counts += result.count
        self._results.append(result)

    def pretty(self, filter: list[TestFilter], indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []

        if TestFilter.NONE not in filter:
            if TestFilter.TOTALS in filter or TestFilter.OVERALL in filter:
                passed, failed, skipped = self.count.total
                totals = f"\[{ResultTypes.PASSED.color}{passed}[@F]:{ResultTypes.SKIPPED.color}{skipped}[@F]\
:{ResultTypes.FAILED.color}{failed}[@F]]"
                out.append(" " * indent + f"*{totals} {TED.encode(self.name)}")

            if TestFilter.OVERALL not in filter:
                if len(self.results):
                    for result in self.results:
                        out.extend(result.pretty(filter=filter, indent=indent + 4))
                else:
                    out.append(
                        " " * (indent + 4)
                        + f"[@Fyellow]No tests found for {TED.encode(self.name)}"
                    )

        return out

    def str(self, indent: int = 0) -> list:
        """Results formatted into lines without colors

        Args:
            indent (int, optional): The amount to indent the lines. Defaults to 0.

        Returns:
            list: The results as lines
        """
        out = []

        passed, failed, skipped = self.count.total
        out.append(" " * indent + f"[S:{passed}:{skipped}:{failed}] {self.name}")

        if len(self.results):
            for result in self.results:
                out.extend(result.str(indent + 4))
        else:
            out.append(" " * (indent + 4) + f"No tests found for {self.name}")

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """

        out = {self.name: {"type": "Suite", "results": []}}

        for result in self.results:
            out[self.name]["results"].append(result.dict())

        return out

    def csv(self) -> list:
        """The test case results. Each index is a different line in the file

        Returns:
            list: The lines to be written to a CSV file
        """

        out = []

        for result in self.results:
            if isinstance(result.csv(), list):
                for line in result.csv():
                    out.append(f"{self.name}," + line)
            else:
                out.append(f"{self.name},," + result.csv())

        return out

    def save(
        self, location: str = "", ext: Union[str, list[str]] = SaveType.CSV
    ) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """

        location = self.isdir(location)

        if isinstance(ext, str):
            self.__save_to_file(location, ext)
        elif isinstance(ext, list):
            for ext in ext:
                self.__save_to_file(location, ext)
        return True

    def __save_to_file(self, location: str, type: str) -> bool:
        """Saves the data to a given file type in a given location

        Args:
            location (str): Where to save the file
            type (str): Type of file to save, CSV, JSON, TXT

        Returns:
            bool: True if file was saved
        """

        if location is not None:
            with open(location + self.name + type, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Suite, Test Class,Test Case,Result,Info\n")
                    for line in self.csv():
                        file.write(f"{line}\n")
                    return True
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                    return True
                elif type == SaveType.TXT:
                    file.write(repr(self))
                    return True
        else:
            return False

    def __str__(self):
        return "\n".join(self.pretty(filter=[TestFilter.OVERALL]))

    def __repr__(self):
        return "\n".join(self.str())


class RunResults(Result):
    def __init__(self, name: str = "TestRun"):
        super().__init__()

        self._name = name
        self._results = []

    @property
    def results(self) -> list:
        return self._results

    def append(self, result: SuiteResult):
        """Add a result to the list of results. This will also increment the counts.

        Args:
            result (Union[TestResult, ClassResult]): The result to add to the colleciton of results
        """
        self._counts += result.count

        self._results.append(result)

    def pretty(self, filter: list[TestFilter], indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []

        if TestFilter.NONE not in filter:
            if TestFilter.OVERALL in filter or TestFilter.TOTALS in filter:
                passed, failed, skipped = self.count.total
                totals = f"\[{ResultTypes.PASSED.color}{passed}[@F]:{ResultTypes.SKIPPED.color}{skipped}[@F]\
:{ResultTypes.FAILED.color}{failed}[@F]]"
                out.append(" " * indent + f"*{totals} {TED.encode(self.name)}")

            if TestFilter.OVERALL not in filter:
                if len(self.results):
                    for result in self.results:
                        out.extend(result.pretty(filter=filter, indent=indent + 4))
                else:
                    out.append(
                        " " * (indent + 4) + f"[@Fyellow]No tests found for current run"
                    )

        return out

    def str(self, indent: int = 0) -> list:
        """Results formatted into lines without colors

        Args:
            indent (int, optional): The amount to indent the lines. Defaults to 0.

        Returns:
            list: The results as lines
        """
        out = []

        passed, failed, skipped = self.count.total
        out.append(" " * indent + f"[R:{passed}:{skipped}:{failed}] {self.name}")

        if len(self.results):
            for result in self.results:
                out.extend(result.str(indent + 4))
        else:
            out.append(" " * (indent + 4) + f"No tests found for current run")

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """

        out = {self.name: {"type": "Run", "results": []}}

        for result in self.results:
            out[self.name]["results"].append(result.dict())

        return out

    def csv(self) -> list:
        """The test case results. Each index is a different line in the file

        Returns:
            list: The lines to be written to a CSV file
        """

        out = []

        for result in self.results:
            out.extend(result.csv())

        return out

    def save(
        self, location: str = "", ext: Union[str, list[str]] = SaveType.CSV
    ) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """

        location = self.isdir(location)

        if isinstance(ext, str):
            self.__save_to_file(location, ext)
        elif isinstance(ext, list):
            for ext in ext:
                self.__save_to_file(location, ext)
        return True

    def __save_to_file(self, location: str, type: str) -> bool:
        """Saves the data to a given file type in a given location

        Args:
            location (str): Where to save the file
            type (str): Type of file to save, CSV, JSON, TXT

        Returns:
            bool: True if file was saved
        """

        if location is not None:
            with open(location + self.name + type, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Suite, Test Class,Test Case,Result,Info\n")
                    for line in self.csv():
                        file.write(f"{line}\n")
                    return True
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                    return True
                elif type == SaveType.TXT:
                    file.write(repr(self))
                    return True
        else:
            return False

    def __str__(self):
        return "\n".join(self.pretty([TestFilter.OVERALL]))

    def __repr__(self):
        return "\n".join(self.str())
