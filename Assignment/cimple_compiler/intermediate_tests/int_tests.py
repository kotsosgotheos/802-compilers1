from cimple_tests.test_helper import *;

class FinalTests:
    def __init__(self):
        self.tests = [
            # "intermediate_tests/ex1.ci",
            # "intermediate_tests/exams.ci",
            # "intermediate_tests/max.ci",
            "intermediate_tests/test1.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            # try:
            p = cimple.Parser(test);
            print(p.qlist);
            # except Exception:
                # continue;

FinalTests();
