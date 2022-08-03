from teddecor.UnitTest import TestSuite
from test_colors import *

if __name__ == "__main__":
    TestSuite(
        "TED",
        [Colors, encoding],
    ).run().save(location="./output", ext=SaveType.ALL())
