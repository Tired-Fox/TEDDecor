from teddecor.UnitTest import *
from teddecor import TED
from teddecor.TED.exception import MacroMissingError


class Links(Test):
    @test
    def normal_link(self):
        link = "https://example.com"
        result = TED.parse(f"[~{link}]")
        assertThat(
            result, eq(f"\x1b]8;;{link}\x1b\\{link}\x1b[0m\x1b]8;;\x1b\\\x1b[0m")
        )

    @test
    def pretty_link(self):
        link = "https://example.com"
        result = TED.parse(f"[~{link}|example]")
        assertThat(
            result, eq(f"\x1b]8;;{link}\x1b\\example\x1b[0m\x1b]8;;\x1b\\\x1b[0m")
        )

    @test
    def pretty_link_nested(self):
        link = "https://example.com"
        result = TED.parse(f"[~{link}|[@F red]example]")
        assertThat(
            result,
            eq(f"\x1b]8;;{link}\x1b\\\x1b[31mexample\x1b[0m\x1b]8;;\x1b\\\x1b[0m"),
        )


@test
def pretty_link_no_markup():
    link = "https://example.com"
    assertThat(wrap(TED.parse, f"[~{link}|]"), raises(MacroMissingError))


if __name__ == "__main__":
    Links().run()
    run(pretty_link_no_markup)
