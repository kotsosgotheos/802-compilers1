from cimple_tests.test_helper import *;

class ReturnStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/return1.ci",
            "cimple_tests/return2.ci",
            "cimple_tests/return3.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

ReturnStatTest();
