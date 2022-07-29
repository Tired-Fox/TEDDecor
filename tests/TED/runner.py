from teddecor.UnitTest import TestSuite
from test_colors import *
from test_func import *
from test_links import *

if __name__ == "__main__":
    suite = (
        TestSuite(
            "TED",
            [
                Colors,
                ColorExceptions,
                Builtin,
                BuiltinExceptions,
                Links,
                pretty_link_no_markup,
            ],
        )
        .run()
        .save(location="./output", ext=SaveType.ALL())
    )
