#
# Get direction
# If more entries than config defined width and is vertical then swap to horizontal
# If horizontal
#       height = num of entries + 2
# If vertical
#       height = config set height + 2. Defaults to 10

from shutil import get_terminal_size
from typing import Union
from ..TED.markup import TED
from math import ceil

from .objects import Config, Entry, Entries


class Graph:
    def __init__(self, entries: Union[list[Entry], Entries], config: Config):
        if isinstance(entries, list):
            entries = Entries(entries)

        self._config = config
        self._entries = entries

        width, height = get_terminal_size()

        self._left_buffer = self.get_buffer()
        self._w = (width * (config["width"] // 100)) - self._left_buffer - 1

        if len(entries) >= self._w and config["dir"] == "v":
            config["dir"] = "v"

        if config["dir"] == "h":
            self._h = len(entries)
        elif config["dir"] == "v":
            self._h = config["height"]

        self._scale = self.scale()

    def scale(self) -> int:
        max_value = self.max([item.value for item in self._entries])
        return max_value / (self._w - self.get_buffer())

    def max(self, items: list) -> int:
        max = -1
        for item in items:
            if item > max:
                max = item
        return max

    def pretty(self) -> str:
        entries = ",\n".join(
            "        " + "\n        ".join(entry.pretty()) for entry in self._entries
        )
        yield "Graph("
        yield f"    width: {self._w},"
        yield f"    height: {self._h},"
        yield f"    scale: {self._scale},"
        yield f"    name buffer: {self._left_buffer},"
        yield f"    entries: [\n{entries}\n    ]"
        yield ")"

    def __repr__(self) -> str:
        return f"Graph(width: {self._w}, height: {self._h}, entries: {self._entries})"

    def __getitem__(self, index: Union[int, slice, tuple[str]]) -> str:
        if self._config["dir"] == "h":
            return self.get_horizontal(index)
        elif self._config["dir"] == "v":
            return self.get_vertical(index)

    def __str__(self) -> str:
        return self[:]

    def get_buffer(self) -> int:
        if self._config["dir"] == "h":
            return (
                self.max([len(item.name + str(f" [{item.value}]")) for item in entries])
                + 1
            )
        elif self._config["dir"] == "v":
            return self.max([len(item.name) for item in entries]) + 1

    def get_horizontal(self, index: Union[int, slice]) -> str:
        def get_bar() -> str:
            step = 4

            bar = "".join(
                "┬".rjust(step, "─")
                for i in range(0, self._w - self._left_buffer, step)
            )
            bar += "╯".rjust(step, "─")
            bar = " " * (self._left_buffer) + "╰" + bar

            num_lead = " " * (self._left_buffer + 1)
            numbers = []
            nums = [
                str(round(num * self._scale))
                for num in range(step, self._w - self._left_buffer + step, step)
            ]

            length = self.max([len(num) for num in nums])
            for i in range(length):
                out = []
                for num in nums:
                    if len(num) > i:
                        out.append(num[i].rjust(step, " "))
                    else:
                        out.append(" ".rjust(step, " "))
                numbers.append(num_lead + "".join(out))

            numbers = "\n".join(numbers)
            return f"{bar}\n{numbers}"

        if isinstance(index, (int, str)):
            entry = self._entries[index]
            label = (
                entry.name
                + f"\[{entry.value}]".rjust(self._left_buffer - len(entry.name), " ")
                + " "
            )
            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            output.append(
                TED.parse(
                    f"{label}[@F]┤{entry.color}"
                    + ("█" * ceil(entry.value / self._scale))
                )
            )
            output.append(get_bar())
            output.append(f"")
            return "\n".join(output)
        elif isinstance(index, (slice, tuple)):
            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            for entry in self._entries[index]:
                label = (
                    entry.name
                    + f"\[{entry.value}]".rjust(
                        self._left_buffer - len(entry.name), " "
                    )
                    + " "
                )
                output.append(
                    TED.parse(
                        f"{label}[@F]┤{entry.color}"
                        + ("█" * ceil(entry.value / self._scale))
                    )
                )
            output.append(get_bar())
            return "\n".join(output)

    def get_vertical(self, index: Union[int, slice, str, tuple[str]]) -> str:
        def get_bar(entries: list, buffer: int, entry_width: int) -> str:
            spacing = "".ljust(buffer, " ")
            half = entry_width // 2
            segment = (
                lambda x, filler: f"{''.ljust(half, filler)}{x}{''.ljust(half, filler)}"
            )
            bar = f"{spacing}╰{''.join(segment('┬', '─') for i in range(len(entries)))}"
            bar = bar[:-1] + "╯"
            spacing += " "
            # bar += f"\n{spacing}{''.join(segment(TED.parse(f'{entry.color}●'), ' ') for entry in entries)}\n"
            bar += "\n" + spacing
            for entry in entries:
                half_value = half - (len(str(entry.value)) + 2) // 2
                bar += f"{''.ljust(half_value, ' ')}[{TED.parse(entry.color + str(entry.value))}]{''.ljust(half_value, ' ')}"

            names = []
            length = self.max([len(entry.name) for entry in entries])
            for i in range(length):
                out = []
                for entry in entries:
                    if len(entry.name) > i:
                        out.append(segment(entry.name[i], " "))
                    else:
                        out.append(segment(" ", " "))
                names.append(spacing + "".join(out))

            names = "\n".join(names)
            return bar + "\n" + names

        total = self.max([elem.value for elem in self._entries])
        vscale = total / self._h
        nums = [str(round(num * vscale)) for num in range(1, self._h + 1)]

        buffer = self.max([len(elem) for elem in nums]) + 1

        if isinstance(index, (int, str)):
            entry_width = self._w - buffer
            entry = self._entries[index]

            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            row = self._h - 1
            while row > -1:
                out = [nums[row].ljust(buffer, " ") + "┤"]
                if entry.value >= total - (row * vscale):
                    out.append(TED.parse(entry.color + "".ljust(entry_width, "█")))
                else:
                    out.append(TED.parse("".ljust(entry_width, " ")))
                output.append("".join(out))
                row -= 1
            output.append(self._entries[index], buffer, entry_width)
            return "\n".join(output)
        elif isinstance(index, (slice, tuple)):
            entry_width = (self._w // len(self._entries[index])) - buffer

            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            row = self._h - 1
            while row > -1:
                out = [nums[row].ljust(buffer, " ") + "┤"]
                for entry in self._entries[index]:
                    if entry.value >= (row * vscale):
                        out.append(TED.parse(entry.color + "".ljust(entry_width, "█")))
                    else:
                        out.append(TED.parse("".ljust(entry_width, " ")))
                output.append("".join(out))
                row -= 1
            output.append(get_bar(self._entries[index], buffer, entry_width))
            return "\n".join(output)


class InlineGraph(Graph):
    def scale(self) -> int:
        self.sum = sum([item.value for item in self._entries])
        return (self._w - self.get_buffer()) / self.sum

    def get_buffer(self) -> int:
        return 2

    def get_horizontal(self, index: Union[int, slice]) -> str:
        if isinstance(index, (int, str)):
            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            output.append("╭" + "─" * self._w + "╮")
            entry = self._entries[index]
            output.append(
                TED.parse(
                    f"│{entry.color}"
                    + (("█" * ceil(entry.value * self._scale)) - 1).ljust(self._w, " ")
                    + "[@F]│"
                )
            )
            output.append("╰" + "─" * self._w + "╯")

            output.append(
                TED.parse(
                    f"{entry.color}● {entry.value} {entry.name} ({round((entry.value/self.sum) * 100, 2)}%)"
                )
            )
            return "\n".join(output)
        elif isinstance(index, (slice, tuple)):
            output = (
                [TED.parse(f"*{TED.encode(self._config['name'])}")]
                if self._config["name"] != ""
                else []
            )
            output.append("╭" + "─" * self._w + "╮")
            values = []
            key = []
            for entry in self._entries[index]:
                values.append(
                    TED.parse(entry.color + ("█" * ceil(entry.value * self._scale)))
                )
                key.append(
                    TED.parse(
                        f"{entry.color}● {entry.value} {entry.name} ({round((entry.value/self.sum) * 100, 2)}%)"
                    )
                )
            output.append(
                "│"
                + "".join(values)
                + " " * (self._w - len(TED.strip("".join(values))))
                + "│"
            )
            output.append("╰" + "─" * self._w + "╯")
            output.append(" " + "\n ".join(key))
            return "\n".join(output)

    def get_vertical(self, index: Union[int, slice, str, tuple[str]]) -> str:
        return self.get_horizontal(index)


if __name__ == "__main__":
    entries = Entries(
        [
            Entry("Passed", 145, "[@F green]"),
            Entry("Skipped", 5, "[@F yellow]"),
            Entry("Failed", 3, "[@F red]"),
        ]
    )
    # bargraph = Graph(entries, Config(dir="v", height=10))
    # print(bargraph[:])
    inlinegraph = InlineGraph(entries, Config())
    print(inlinegraph)
