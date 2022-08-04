from teddecor.UnitTest import *
from teddecor import TED
from teddecor.TED.exception import MacroError


class Colors(Test):
    @test
    def foreground(self):
        result = TED.parse("[@F red] foreground color")
        assertThat("\x1b[31m foreground color\x1b[0m", eq(result))

    @test
    def background(self):
        result = TED.parse("[@B red] background color")
        assertThat("\x1b[41m background color\x1b[0m", eq(result))

    @test
    def foreground_and_background(self):
        result = TED.parse("[@F green @B red] foreground and background color")
        assertThat("\x1b[32;41m foreground and background color\x1b[0m", eq(result))

    @test
    def predefined_color(self):
        result = TED.parse("[@F red] predefined color")
        assertThat("\x1b[31m predefined color\x1b[0m", eq(result))

    @test
    def xterm_color(self):
        result = TED.parse("[@F 7] xterm color")
        assertThat("\x1b[38;5;7m xterm color\x1b[0m", eq(result))

    @test
    def rgb_color(self):
        result = TED.parse("[@F 213,14,124] RGB color")
        assertThat("\x1b[38;2;213;14;124m RGB color\x1b[0m", eq(result))

        result = TED.parse("[@F 213;14,124] RGB color")
        assertThat("\x1b[38;2;213;14;124m RGB color\x1b[0m", eq(result))

    @test
    def hex_color(self):
        result = TED.parse("[@F #EBA937] hex color")
        assertThat("\x1b[38;2;235;169;55m hex color\x1b[0m", eq(result))

    @test
    def reset_foreground(self):
        result = TED.parse("[@F Red]Color[@F] reset")
        assertThat("\x1b[31mColor\x1b[39m reset\x1b[0m", eq(result))

    @test
    def reset_background(self):
        result = TED.parse("[@B Red]Color[@B] reset")
        assertThat("\x1b[41mColor\x1b[49m reset\x1b[0m", eq(result))

    @test
    def reset_foreground_and_background(self):
        result = TED.parse("[@F red @B Red]Color[@] reset")
        assertThat("\x1b[31;41mColor\x1b[39;49m reset\x1b[0m", eq(result))

    @test
    def assign_both(self):
        result = TED.parse("[@ red]Assing fg and bg")
        assertThat("\x1b[31;41mAssing fg and bg\x1b[0m", eq(result))

    @test
    def optimizations(self):
        result = TED.parse("[@ red @B white]*Optimize **format ansi")
        assertThat("\x1b[1;31;47mOptimize format ansi\x1b[0m", eq(result))


class ColorExceptions(Test):
    @test
    def not_in_predefined(self):
        assertThat(wrap(TED.parse, "[@F bad]Bad"), raises(MacroError))

    @test
    def no_specifier(self):
        assertThat(wrap(TED.parse, "[@ bad]Bad"), raises(MacroError))
