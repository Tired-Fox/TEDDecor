from teddecor.UnitTest import *
from teddecor import TED


class HLink(Test):
    def __init__(self):
        self.link = "https://example.com"
        self.open = f"\x1b]8;;{self.link}\x1b\\"
        self.close = "\x1b]8;;\x1b\\"
        self.reset = "\x1b[0m"

    @test
    def auto_close(self):
        result = TED.parse(f"[~{self.link}]Example")
        assertThat(result, eq(f"{self.open}Example{self.close}{self.reset}"))

    @test
    def manual_close(self):
        result = TED.parse(f"[~{self.link}]Example[~]")
        assertThat(result, eq(f"{self.open}Example{self.close}{self.reset}"))

    @test
    def auto_close_between_links(self):
        result = TED.parse(f"[~{self.link}]Example [~{self.link}]Example2")
        assertThat(
            result,
            eq(
                f"{self.open}Example {self.close}{self.open}Example2{self.close}{self.reset}"
            ),
        )
