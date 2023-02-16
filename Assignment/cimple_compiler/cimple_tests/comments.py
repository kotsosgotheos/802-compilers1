from cimple_tests.test_helper import *

class CommentsTest:
    def __init__(self):
        self.tests = [
            "cimple_tests/comments.ci",
        ];

        for test in self.tests:
            print(f"Testing: {test}");
            try:
                l = cimple.Lexer(test);
                print(len(l.token_table) == 0);
            except Exception:
                continue;

CommentsTest();
