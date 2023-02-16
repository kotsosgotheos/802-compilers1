from cimple_tests.test_helper import *;

class CallStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/call1.ci",
            "cimple_tests/call2.ci",
            "cimple_tests/call3.ci",
            "cimple_tests/call4.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

CallStatTest();
