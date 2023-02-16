import sys
sys.path.append("../");
import cimple

class Test2Test:
    def __init__(self):
        print("Testing: test2.ci");
        l = cimple.Lexer("cimple_tests/test2.ci");
        print("".join(l.file_text) == "hello\nworld\noblivious42.");

Test2Test();
