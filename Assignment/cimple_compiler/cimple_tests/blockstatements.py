from cimple_tests.test_helper import *

class BlockstatementsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/blockstatements1.ci",
            "cimple_tests/blockstatements2.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

BlockstatementsTest();
