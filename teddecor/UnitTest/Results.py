"""Results

TestResults, ClassResults, and SuiteResults all hold and translate the test result information
into a structure that is easy to use and has mutliple outputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union, Callable


__all__ = ["TestResult", "ClassResult", "SuiteResult", "SaveType", "ResultType"]


@dataclass
class ResultType:
    """Enum/Dataclass that describes the test run result.

    Attributes:
        SUCCESS (tuple[str, str]): Message and color for a successful test run
        FAILED (tuple[str, str]): Message and color for a failed test run
        SKIPPED (tuple[str, str]): Message and color for a skipped test run
    """

    SUCCESS: tuple[str, str, int] = ("Passed", "\x1b[1;32m", "✓")
    FAILED: tuple[str, str, int] = ("Failed", "\x1b[1;31m", "x")
    SKIPPED: tuple[str, str, int] = ("Skipped", "\x1b[1;33m", "↻")


@dataclass
class SaveType:
    CSV: str = ".csv"
    JSON: str = ".json"
    TXT: str = ".txt"


class Result:
    """Base class for result types"""

    def __init__(self):
        self._counts = [0, 0, 0]

    @property
    def counts(self) -> tuple[int, int, int]:
        """Get counts for passed, failed, skipped.

        Returns:
            tuple: The values for passed, failed, skipped respectively
        """
        return tuple(self._counts)

    @property
    def name(self) -> str:
        return self._name

    def write(self, indent: int = 0):
        """Output the result(s) to the screen

        Args:
            indent (int, optional): The amount to indent the values. Defaults to 0.
        """
        for line in self.pretty(indent):
            print(line)

    def pretty(self) -> list:
        """Format the result(s) into a formatted list

        Returns:
            list: List of formatted result(s)
        """
        return []

    def dict(self) -> dict:
        return {}

    def isdir(self, location: str) -> bool:
        """Takes the location that the file is to be saved then changes directory.

        Args:
            location (str, optional): The location where the file will be saved. Defaults to None.

        Returns:
            bool: Whether the directory exists

        Note:
            This is to be used with an inherited class and will auto convert `~` to it's absolute path
        """

        if location != "":
            from os import path

            if location.startswith("~"):
                from pathlib import Path

                location = str(Path.home()) + location[1:]

            if not path.isdir(location):
                return False
            else:
                return True

        return True


class TestResult(Result):
    def __init__(self, result: tuple[str, ResultType, Union[str, list]] = None):
        super().__init__()

        if result is not None:
            self._name = result[0]
            self._result = result[1]
            self._info = result[2]
        else:
            self._name = "Unknown"
            self._result = ResultType.SKIPPED
            self._info = "Unkown test"

        if result[1] == ResultType.SUCCESS:
            self._counts[0] += 1
        elif result[1] == ResultType.FAILED:
            self._counts[1] += 1
        elif result[1] == ResultType.SKIPPED:
            self._counts[2] += 1

    @property
    def result(self) -> str:
        return self._result[0]

    @property
    def color(self) -> str:
        return self._result[1]

    @property
    def icon(self) -> str:
        return self._result[2]

    @property
    def info(self) -> Union[str, list]:
        return self._info

    def pretty(self, indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []
        out.append(
            " " * indent + f"[{self.color}{self.icon}\x1b[0m] <case> {self.name}"
        )
        if isinstance(self.info, list):
            for trace in self.info:
                out.append(" " * (indent + 4) + trace)
        else:
            if self.info != "":
                out.append(" " * (indent + 4) + self.info)

        return out

    def str(self, indent: int = 0) -> list:
        out = []
        out.append(" " * indent + f"[{self.icon}] <case> {self.name}")
        if isinstance(self.info, list):
            for trace in self.info:
                out.append(" " * (indent + 4) + trace)
        else:
            out.append(self.info)

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """
        return {self.name: {"result": self._result[0], "info": self.info}}

    def csv(self) -> str:
        info = "\n".join(self.info) if isinstance(self.info, list) else self.info
        return f"{self.name},{self.result},'{info}'"

    def save(self, location: str = "", type: str = SaveType.CSV) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """
        ext = type

        if super().isdir(location):
            with open(location + self.name + ext, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Case,result,info\n")
                    file.write(self.csv())
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                elif type == SaveType.TXT:
                    file.write(repr(self))
        else:
            return False

        return True

    def __str__(self):
        return "\n".join(self.pretty())

    def __repr__(self):
        return "\n".join(self.str())


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
        passed, failed, skipped = result.counts
        self._counts[0] += passed
        self._counts[1] += failed
        self._counts[2] += skipped

        self._results.append(result)

    def pretty(self, indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []

        passed, failed, skipped = self.counts
        totals = f"\x1b[1m[{ResultType.SUCCESS[1]}{passed}\x1b[37m:{ResultType.SKIPPED[1]}{skipped}\x1b[37m\
:{ResultType.FAILED[1]}{failed}\x1b[37m]\x1b[0m"
        out.append(" " * indent + f"{totals} \x1b[1m<class> {self.name}\x1b[0m")

        if len(self.results):
            for result in self.results:
                out.extend(result.pretty(indent + 4))
        else:
            out.append(
                " " * (indent + 4) + f"\x1b[1;33mNo Tests Found for {self.name}\x1b[0m"
            )

        return out

    def str(self, indent: int = 0) -> list:
        out = []

        passed, failed, skipped = self.counts
        out.append(" " * indent + f"[{passed}:{skipped}:{failed}] <class> {self.name}")

        if len(self.results):
            for result in self.results:
                out.append("".join(result.str(indent + 4)))
        else:
            out.append(" " * (indent + 4) + f"No Tests Found for {self.name}")

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """

        out = {self.name: {}}

        for result in self.results:
            out[self.name].update(result.dict())

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

    def save(self, location: str = "", type: str = SaveType.CSV) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """
        ext = type

        if super().isdir(location):
            with open(location + self.name + ext, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Class,Test Case,Result,Info\n")
                    for line in self.csv():
                        file.write(f"{line}\n")
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                elif type == SaveType.TXT:
                    file.write(repr(self))
        else:
            return False

        return True

    def __str__(self):
        return "\n".join(self.pretty())

    def __repr__(self):
        return "\n".join(self.str())


class SuiteResult(Result):
    def __init__(self, name: str):
        super().__init__()

        self._name = name
        self._results = []

    @property
    def results(self) -> list:
        return self._results

    def append(self, result: Union[TestResult, ClassResult]):
        passed, failed, skipped = result.counts
        self._counts[0] += passed
        self._counts[1] += failed
        self._counts[2] += skipped

        self._results.append(result)

    def pretty(self, indent: int = 0) -> list:
        """Used to convert results into a list of strings. Allows for additional indentation to be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            list: The formatted results as a list of string with indents
        """

        out = []

        passed, failed, skipped = self.counts
        totals = f"\x1b[1m[{ResultType.SUCCESS[1]}{passed}\x1b[37m:{ResultType.SKIPPED[1]}{skipped}\x1b[37m\
:{ResultType.FAILED[1]}{failed}\x1b[37m]\x1b[0m"
        out.append(" " * indent + f"{totals} \x1b[1m<suite> {self.name}\x1b[0m")

        if len(self.results):
            for result in self.results:
                out.extend(result.pretty(indent + 4))
        else:
            out.append(
                " " * (indent + 4) + f"\x1b[1;33mNo Tests Found for {self.name}\x1b[0m"
            )

        return out

    def str(self, indent: int = 0) -> list:
        out = []

        passed, failed, skipped = self.counts
        out.append(" " * indent + f"[{passed}:{skipped}:{failed}] <suite> {self.name}")

        if len(self.results):
            for result in self.results:
                out.append("".join(result.str(indent + 4)))
        else:
            out.append(" " * (indent + 4) + f"No Tests Found for {self.name}")

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """

        out = {self.name: {}}

        for result in self.results:
            out[self.name].update(result.dict())

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
                out.append(f"{self.name}," + result.csv())

        return out

    def save(self, location: str = "", type: str = SaveType.CSV) -> bool:
        """Takes a file location and creates a json file with the test data

        Args:
            location (str, optional): The location where the json file will be created. Defaults to "".

        Returns:
            bool: True if the file was successfully created
        """
        ext = type

        if super().isdir(location):
            with open(location + self.name + ext, "+w", encoding="utf-8") as file:
                if type == SaveType.CSV:
                    file.write("Test Class,Test Case,Result,Info\n")
                    for line in self.csv():
                        file.write(f"{line}\n")
                elif type == SaveType.JSON:
                    from json import dumps

                    file.write(dumps(self.dict(), indent=2))
                elif type == SaveType.TXT:
                    file.write(repr(self))
        else:
            return False

        return True

    def __str__(self):
        return "\n".join(self.pretty())

    def __repr__(self):
        return "\n".join(self.str())
