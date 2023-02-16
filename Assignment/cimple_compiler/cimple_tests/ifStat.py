from cimple_tests.test_helper import *;

class IfStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/if1.ci",
            "cimple_tests/if2.ci",
            "cimple_tests/if3.ci",
            "cimple_tests/if4.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

IfStatTest();
