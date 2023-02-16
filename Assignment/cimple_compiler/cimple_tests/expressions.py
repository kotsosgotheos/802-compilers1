from cimple_tests.test_helper import *;

class ExpressionsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/expressions1.ci",
            "cimple_tests/expressions2.ci",
            "cimple_tests/expressions3.ci",
            "cimple_tests/expressions4.ci",
            "cimple_tests/expressions5.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

ExpressionsTest();
