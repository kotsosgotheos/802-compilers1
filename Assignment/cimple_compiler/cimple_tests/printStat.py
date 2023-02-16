from cimple_tests.test_helper import *;

class PrintStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/print1.ci",
            "cimple_tests/print2.ci",
            "cimple_tests/print3.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

PrintStatTest();
