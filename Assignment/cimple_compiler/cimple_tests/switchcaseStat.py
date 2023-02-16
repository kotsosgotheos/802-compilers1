from cimple_tests.test_helper import *;

class SwitchcaseStat:
    def __init__(self):
        self.tests = [
            "cimple_tests/switchcase1.ci",
            "cimple_tests/switchcase2.ci",
            "cimple_tests/switchcase3.ci",
            "cimple_tests/switchcase4.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

SwitchcaseStat();
