from cimple_tests.test_helper import *;

class FinalTests:
    def __init__(self):
        self.tests = [
            "final_tests2/_armstrong.ci",
            "final_tests2/_factorialnew.ci",
            "final_tests2/_HappyDay.ci",
            "final_tests2/_max3.ci",
            "final_tests2/_pap.ci",
            "final_tests2/_power.ci",
            "final_tests2/_test_parser.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

FinalTests();
