from teddecor.UnitTest import *


@test
def _12_eq_12():
    assertThat(12, eq(12))


if __name__ == "__main__":
    # assertThat(None, _is(12))
    run(_12_eq_12).save(ext=SaveType.TXT)
    # print(TED.strip("\[[@F red]Error Message[@F]] \x1b[1m*Some error \\_message"))
