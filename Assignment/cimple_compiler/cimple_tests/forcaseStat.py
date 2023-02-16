from cimple_tests.test_helper import *;

class ForcaseStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/forcase1.ci",
            "cimple_tests/forcase2.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

ForcaseStatTest();
