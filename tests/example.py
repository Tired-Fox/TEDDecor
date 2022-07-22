from teddecor.UnitTest import *

class Testing(UnitTest):
    def __init__(self):
        test = UnitTest()
        
    @test
    def example_1(self):
        assert True

    @test
    def example_2(self):
        assert False


if __name__ == "__main__":
    Testing().main()
