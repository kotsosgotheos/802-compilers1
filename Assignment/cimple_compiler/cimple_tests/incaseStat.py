from cimple_tests.test_helper import *;

class IncaseStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/incase1.ci",
            "cimple_tests/incase2.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

IncaseStatTest();
