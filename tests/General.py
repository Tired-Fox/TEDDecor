from teddecor.UnitTest import *


class Testing(Test):
    @test
    def _12_eq_12(self):
        assertThat(12, eq(12))


if __name__ == "__main__":
    TestSuite("Suite Filtering", tests=[Testing]).run()
    Testing().run()
    run(Testing()._12_eq_12)
