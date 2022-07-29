from teddecor.UnitTest import *
from teddecor.TED import parse
from teddecor.TED.exception import *
from teddecor.TED.colors import XTERM


class Builtin(Test):
    @test
    def rainbow(self):
        colors = [
            f"\x1b[{XTERM(30, 196)}m",
            f"\x1b[{XTERM(30, 202)}m",
            f"\x1b[{XTERM(30, 190)}m",
            f"\x1b[{XTERM(30, 41)}m",
            f"\x1b[{XTERM(30, 39)}m",
            f"\x1b[{XTERM(30, 92)}m",
        ]
        string = "rainbow"
        result = parse(f"[^rainbow|{string}]")
        against = ""
        for i, char in enumerate(string):
            against += f"{colors[i%len(colors)]}{char}"

        against += "\x1b[39;49m\x1b[0m"
        assertThat(result, eq(against))

    @test
    def repr(self):
        result = parse(f"[^repr|test_result]")
        assertThat(result, eq("'test_result'\x1b[0m"))

    @test
    def repr(self):
        result = parse(f"[^esc|test_result]")
        assertThat(result, eq("test_result\x1b[0m"))


class BuiltinExceptions(Test):
    @test
    def does_not_exist(self):
        assertThat(wrap(parse, "[^bad|Bad]"), raises(MacroError))

    @test
    def requires_input(self):
        assertThat(wrap(parse, "[^rainbow]"), raises(MacroMissingError))


if __name__ == "__main__":
    Builtin().run()
    BuiltinExceptions().run()
