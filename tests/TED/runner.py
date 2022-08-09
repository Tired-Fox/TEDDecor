from teddecor.UnitTest import *
from teddecor import TED


@test
def test_encoding() -> None:
    """Test the encoding of markup characters."""
    encoded_string = TED.encode("_U_*B*[mac]")
    assertThat(encoded_string, eq("\_U\_\*B\*\[mac]"))
