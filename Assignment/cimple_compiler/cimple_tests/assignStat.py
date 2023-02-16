from cimple_tests.test_helper import *

class AssignStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/assignStat1.ci",
            "cimple_tests/assignStat2.ci",
            "cimple_tests/assignStat3.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

AssignStatTest();
