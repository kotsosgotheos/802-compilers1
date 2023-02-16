from cimple_tests.test_helper import *;

class InputStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/input1.ci",
            "cimple_tests/input2.ci",
            "cimple_tests/input3.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

InputStatTest();
