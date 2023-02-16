from cimple_tests.test_helper import *

class DeclarationsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/declarations1.ci",
            "cimple_tests/declarations2.ci",
            "cimple_tests/declarations3.ci",
            "cimple_tests/declarations4.ci",
            "cimple_tests/declarations5.ci",
            "cimple_tests/declarations6.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

DeclarationsTest();
