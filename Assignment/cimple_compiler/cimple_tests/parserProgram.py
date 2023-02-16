from cimple_tests.test_helper import *

class ParserProgramTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/parserProgram.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                cimple.Parser(test);
            except Exception:
                continue;

ParserProgramTest();
