from cimple_tests.test_helper import *

class SubprogramsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/subprograms1.ci",
            "cimple_tests/subprograms2.ci",
            "cimple_tests/subprograms3.ci",
            "cimple_tests/subprograms4.ci",
            "cimple_tests/subprograms5.ci",
            "cimple_tests/subprograms6.ci",
            "cimple_tests/subprograms7.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

SubprogramsTest();
