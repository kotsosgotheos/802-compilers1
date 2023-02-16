from cimple_tests.test_helper import *

class BlocksTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/blocks.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

BlocksTest();
