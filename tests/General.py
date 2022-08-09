from teddecor.UnitTest import *


class Testing(Test):
    @test
    def _12_eq_12(self):
        assertThat(12, eq(12))


if __name__ == "__main__":
    TestSuite("Suite Filtering", tests=[Testing]).run(filter=[TestFilter.TOTALS])
    # Testing().run(filter=[TestFilter.TOTALS, TestFilter.SKIPPED])
