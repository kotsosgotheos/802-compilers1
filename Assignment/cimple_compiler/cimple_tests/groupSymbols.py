from cimple_tests.test_helper import *

class GroupSymbolsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/groupSymbols.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                l = cimple.Lexer(test);
                print(len(l.token_table) == 8);
                for token in l.token_table:
                    print(token);
            except Exception:
                continue;

GroupSymbolsTest();
