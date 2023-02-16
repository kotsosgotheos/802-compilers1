from cimple_tests.test_helper import *;

class FinalTests:
    def __init__(self):
        self.tests = [
            "cimple_tests/final_tests/factorial.ci",
            "cimple_tests/final_tests/fibonacci.ci",
            "cimple_tests/final_tests/countDigits.ci",
            "cimple_tests/final_tests/summation.ci",
            "cimple_tests/final_tests/primes.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

FinalTests();
