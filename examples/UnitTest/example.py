from teddecor.UnitTest import *


class Example(Test):
    @test
    def test_pass(self):
        assert True


if __name__ == "__main__":
    Example().run()
