from teddecor.UnitTest import *
from test_colors import Colors
from test_hlinks import HLink

from teddecor import TED


@test
def test_encoding() -> None:
    """Test the encoding of markup characters."""
    encoded_string = TED.encode("_U_*B*[mac]")
    assertThat(encoded_string, eq("\_U\_\*B\*\[mac]"))


if __name__ == "__main__":
    TestSuite(
        "TED",
        [Colors, HLink, test_encoding],
    ).run().save(location="./output", ext=SaveType.ALL())
