from cimple_tests.test_helper import *;

class WhileStatTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/while1.ci",
            "cimple_tests/while2.ci",
            "cimple_tests/while3.ci",
            "cimple_tests/while4.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

WhileStatTest();
