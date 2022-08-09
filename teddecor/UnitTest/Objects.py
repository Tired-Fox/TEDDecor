from dataclasses import dataclass

__all__ = ["TestFilter"]


@dataclass
class TestFilter:
    OVERALL: int = 1
    TOTALS: int = 2
    PASSED: int = 3
    FAILED: int = 4
    SKIPPED: int = 5
    NONE: int = 6
