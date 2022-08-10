from __future__ import annotations
from teddecor import TED
from typing import Union, Any

__all__ = ["Entries", "Entry", "Config"]


class Entries:
    def __init__(self, entries: list[Entry] = []):
        self._entries = []
        for entry in entries:
            self.append(entry)

    def append(self, entry: Entry) -> None:
        if isinstance(entry, Entry):
            self._entries.append(entry)

    def extend(self, entries: list[Entry]) -> None:
        if isinstance(entries, list):
            for entry in entries:
                self.append(entry)

    def index(self, value: Union[Entry, str]) -> int:
        """Get the Entry's index by name or by equivelant Entry.

        Args:
            value (Union[Entry, str]): The Entry or name/str to search by.

        Returns:
            int: The index where that value is held.
        """
        if isinstance(value, Entry):
            return self._entries.index(value)
        elif isinstance(value, str):
            for i, entry in enumerate(self._entries):
                if entry.name == value:
                    return i

    def __getitem__(self, index) -> Union[Entry, list[Entry]]:
        if isinstance(index, (int, slice)):
            return self._entries[index]
        elif isinstance(index, str):
            return self[self.index(index)]
        elif isinstance(index, tuple):
            output = []
            for item in index:
                if isinstance(item, str):
                    i = self.index(item)
                    if i is not None:
                        output.append(self[i])
            return output

    def __delitem__(self, index: Union[int, str]) -> None:
        if isinstance(index, int):
            del self._entries[index]
        elif isinstance(index, str):
            del self._entries[self.index(index)]

    def __setitem__(self, index: Union[int, str], value: Entry) -> None:
        if isinstance(index, int) and isinstance(value, Entry):
            self._entries[index] = value
        elif isinstance(index, str) and isinstance(value, Entry):
            self._entries[self.index(index)] = value

    def __iter__(self) -> Entries:
        self.curr_index = -1
        return self

    def __next__(self) -> Entry:
        if self.curr_index >= len(self._entries) - 1:
            raise StopIteration
        else:
            self.curr_index += 1
            return self._entries[self.curr_index]

    def __len__(self) -> int:
        return len(self._entries)

    def __repr__(self) -> str:
        return f"[{', '.join(repr(entry) for entry in self._entries)}]"


class Entry:
    def __init__(self, name: str, value: int, color: str) -> None:
        self._name = name
        self._value = value
        self._color = color

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> int:
        return self._value

    @property
    def color(self) -> str:
        return self._color

    def pretty(self) -> str:
        yield "Entry("
        yield f"  name: {self.name},"
        yield f"  value: {self.value},"
        yield f"  color: {self.color}"
        yield f")"

    def __repr__(self) -> str:
        return f"Entry(name: {self.name}, value: {self.value}, color: {self.color})"

    def __str__(self) -> str:
        return TED.parse(f"{self.color}{self.name} - {self.value}")


class Config:
    def __init__(self, **kwargs):
        self._config = {"dir": "h", "width": 100, "height": 10, "name": ""}
        for arg in kwargs:
            if arg in self._config and isinstance(kwargs[arg], type(self._config[arg])):
                self._config[arg] = kwargs[arg]

    @property
    def values(self) -> dict:
        return self._config

    def __getitem__(self, indecies) -> Union[Any, list[Any]]:
        if isinstance(indecies, str):
            return self._config[indecies]
        elif isinstance(indecies, tuple):
            return [self._config[i] for i in indecies]

    def __setitem__(self, index, value) -> None:
        if isinstance(index, str):
            self._config[index] = value


if __name__ == "__main__":
    config = Config(width=50, dir="h")
    print(config["dir", "width"])
