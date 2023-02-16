from cimple_tests.test_helper import *

class FactorialTest:
    def test1(self):
        print("Testing: factorial.ci");
        l = cimple.Lexer("cimple_tests/factorial.ci");
        print("".join(l.file_text) == "program factorial\n{\n\t#declarations#\n\tdeclare x;\n\tdeclare i,fact;\n\n\t#main#\n\tinput(x);\n\tfact:=1;\n\ti:=1;\n\twhile(i<=x)\n\t{\n\t\tfact:=fact*i;\n\t\ti:=i+1;\n\t};\n\tprint(fact);\n}.");
    
    def test2(self):
        print("Testing: factorial.ci");
        l = cimple.Lexer("cimple_tests/factorial.ci");
        lines = l.count_lines();
        print(lines == 17);
    
    def test3(self):
        print("Testing: factorial.ci");
        l = cimple.Lexer("cimple_tests/factorial.ci");
        for token in l.token_table:
            print(token);

    def __init__(self):
        self.test1();
        self.test2();
        self.test3();

FactorialTest();
