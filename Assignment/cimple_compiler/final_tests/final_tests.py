from cimple_tests.test_helper import *;

class FinalTests:
    def __init__(self):
        self.tests = [
            "final_tests/factorial.ci",
            "final_tests/fibonacci.ci",
            "final_tests/countDigits.ci",
            "final_tests/summation.ci",
            "final_tests/primes.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

FinalTests();
