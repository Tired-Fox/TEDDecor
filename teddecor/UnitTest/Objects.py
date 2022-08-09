from dataclasses import dataclass

__all__ = ["TestFilter"]


@dataclass
class TestFilter:
    NONE: int = 0
    OVERALL: int = 1
    TOTALS: int = 2
    PASSED: int = 3
    FAILED: int = 4
    SKIPPED: int = 5

    @staticmethod
    def saslist() -> list[str]:
        return ["none", "overall", "totals", "passed", "failed", "skipped"]

    @staticmethod
    def iaslist() -> list[int]:
        return [i for i in range(6)]
