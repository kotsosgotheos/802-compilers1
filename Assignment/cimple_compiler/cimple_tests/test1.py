import sys
sys.path.append("../");
import cimple

class Test1Test:
    def __init__(self):
        print("Testing: test1.ci");
        l = cimple.Lexer("cimple_tests/test1.ci");
        print("".join(l.file_text) == "hello.");
        print("".join(l.file_text));

Test1Test();
