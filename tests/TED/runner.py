from teddecor.UnitTest import TestSuite
from test_colors import *
from test_links import *

if __name__ == "__main__":
    TestSuite(
        "TED",
        [
            Colors,
            ColorExceptions,
            Links,
        ],
    ).run().save(location="./output", ext=SaveType.ALL())
