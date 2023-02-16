# Konstantinos Georgiou,   4333, cse84333
# Athanasios Papapostolou, 4147, cse74147

import re  # compile, match
import os  # exists
import optparse # OptionParser

EOF = None;

# TODO Check identifer size (30 chars) and integer size (2^(32-1))
KEYWORDS = ["program", "declare", "if", "else", "while", "switchcase", "not", "function", "input", "forcase", "incase", "case", "default", "and", "or", "procedure", "call", "return", "in", "inout", "print"];
REL_OP = ["=", "<=", ">=", ">", "<", "<>"];
ADD_OP = ["+", "-"];
MUL_OP = ["*", "/"];
INTEGER = re.compile("[0-9]+");
ID = re.compile("[a-zA-Z][a-zA-Z0-9]*");

def terminal_match(terminals, str):
    if terminals == KEYWORDS or terminals == REL_OP or terminals == ADD_OP or terminals == MUL_OP:
        return str in terminals;
    elif terminals == INTEGER or terminals == ID:
        m = terminals.match(str);
        if m:
            return True;
        else:
            return False;
    else:
        return None;

class Colored:
    def __init__(self, message):
        self.message = message;

    def red(self):
        return f"\033[1;31m{self.message}\033[0m";

    def green(self):
        return f"\033[1;32m{self.message}\033[0m";

class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string;
        self.family = family;
        self.line_number = line_number;

    def __str__(self):
        return f"{self.recognized_string}\tfamily:\"{self.family}\",\tline: {self.line_number}";

class Lexer:
    def load_file(self, filename):
        characters = [];
        with open(filename, "r") as f:
            while True:
                c = f.read(1);
                characters.append(c);

                if c == "":
                    f.close();
                    return characters;

    def count_lines(self):
        count = 1;
        for c in self.file_text:
            if c == "\n":
                count += 1;
        return count;

    def prev_character(self):
        self.pos -= 1;
        c = self.file_text[self.pos];
        return c;

    def next_character(self):
        self.pos += 1;
        c = self.file_text[self.pos];

        if self.pos == (len(self.file_text) - 1):
            return EOF;
        else:
            return c;

    def error(self, message):
        print(f"{self.filename}:{self.lineno}: {Colored('error:').red()} {message}");
        return [];

    def lex(self):
        token_table = [];

        while(True):
            c = self.next_character();

            if c == EOF:
                break;
            elif c == "\n":
                self.lineno += 1;
            elif c == " " or c == "\t":
                pass;

            elif c == "#":
                c = self.next_character();
                while c != "#":
                    c = self.next_character();
                    if c == "\n":
                        self.lineno += 1;
                    elif c == EOF:
                        return self.error("unterminated # comment");
            elif c.isdigit():
                final_number = c;
                c = self.next_character();
                while c != EOF and c.isdigit():
                    final_number += c;
                    c = self.next_character();
                c = self.prev_character();
                token_table.append(Token(final_number, "number", self.lineno));
            elif c == "+" or c == "-":
                token_table.append(Token(c, "addOperator", self.lineno));
            elif c == "*" or c == "/":
                token_table.append(Token(c, "mulOperator", self.lineno));
            elif c == "{" or c == "}" or c == "(" or c == ")" or c == "[" or c == "]":
                token_table.append(Token(c, "groupSymbol", self.lineno));
            elif c == "," or c == ";" or c == ".":
                token_table.append(Token(c, "delimeter", self.lineno));
            elif c == ":":
                c = self.next_character();
                if c != EOF and c == "=":
                    token_table.append(Token(":=", "assignment", self.lineno));
                else:
                    return self.error("expected '=' after ':' for equality operator.  Maybe you mean ':=' instead?");
            elif c == "<":
                c = self.next_character();
                if c == "=":
                    token_table.append(Token("<=", "relOperator", self.lineno));
                elif c == ">":
                    token_table.append(Token("<>", "relOperator", self.lineno));
                else:
                    c = self.prev_character();
                    token_table.append(Token("<", "relOperator", self.lineno));
            elif c == ">":
                c = self.next_character();
                if c == "=":
                    token_table.append(Token(">=", "relOperator", self.lineno));
                else:
                    self.prev_character();
                    token_table.append(Token(">", "relOperator", self.lineno));
            elif c == "=":
                token_table.append(Token("=", "relOperator", self.lineno));
            elif c.isalpha():
                final_identifier = c;
                c = self.next_character();
                while c != EOF and (c.isdigit() or c.isalpha()):
                    final_identifier += c;
                    c = self.next_character();
                c = self.prev_character();

                if final_identifier in KEYWORDS:
                    token_table.append(Token(final_identifier, "keyword", self.lineno));
                else:
                    token_table.append(Token(final_identifier, "id", self.lineno));

        return token_table;

    def __init__(self, filename):
        self.file_text = self.load_file(filename);
        self.pos = -1;
        self.current_token_pos = -1;
        self.lineno = 1;
        self.filename = filename;

        self.token_table = self.lex();
        if(len(self.token_table) > 0):
            self.current_token = self.token_table[0];
        else:
            self.current_token = None;

    def next_token(self):
        self.current_token_pos += 1;

        if self.current_token_pos >= len(self.token_table):
            return Token("eof", "", self.lineno);
        return self.token_table[self.current_token_pos];

    def prev_token(self):
        self.current_token_pos -= 1;

        if self.current_token_pos == -1:
            return Token("eof", "", self.lineno);
        return self.token_table[self.current_token_pos];

class TempVarSet:
    def __init__(self):
        self.varlist = [];
        self.current = -1;
        self.list = ["T_" + str(self.current)];
    
    def new_temp(self):
        self.current += 1;
        self.list.append("T_" + str(self.current));
        self.varlist.append("T_" + str(self.current));
        return self;
    
    def __str__(self):
        x = self.current;
        return "T_" + str(x);

class Label:
    def __init__(self, labelnum):
        self.labelnum = labelnum;
        self.quad = None;
    
    def __str__(self):
        return f"{self.labelnum}";

class Quad:
    def __init__(self, label, operator, operand1, operand2, operand3):
        self.label = label;
        self.operator = operator;
        self.operand1 = operand1;
        self.operand2 = operand2;
        self.operand3 = operand3;
    
    def __str__(self):
        return f"{self.label}: {self.operator} {self.operand1} {self.operand2} {self.operand3}";

class LabelList:
    def __init__(self, *args):
        if(len(args) == 0):
            self.list = [];
        elif(len(args) == 1):
            self.list = [args[0]];
        else:
            self.list = None;
    
    def merge(self, other):
        new_list = LabelList();
        new_list.list += self.list;
        new_list.list += other.list;
        return new_list;
    
    def backpatch(self, patching_label):
        for label in self.list:
            label.quad.operand3 = patching_label;
    
    def __str__(self):
        ret = "[";

        for i in range(len(self.list) - 1):
            ret += f"{self.list[i]},";
        ret += f"{self.list[-1]}";
        
        ret += "]";
        return ret;

class QuadList:
    def __init__(self):
        self.list = {};
        self.labelcount = 0;
        self.curr_label = Label(self.labelcount + 1);

    def next_quad(self):
        return self.curr_label;
    
    def gen_quad(self, operator, operand1, operand2, operand3):
        # Set quad pointer and add new item to list
        new_quad = Quad(self.curr_label, operator, operand1, operand2, operand3);
        self.curr_label.quad = new_quad;
        self.list[self.curr_label.labelnum] = new_quad;

        # Set next label pointer
        self.labelcount += 1;
        self.curr_label = Label(self.labelcount + 1);
    
    def __str__(self):
        ret = "";

        for item in self.list:
            ret += f"{self.list[item]}\n";
        
        return ret;

class Parser:
    def error(self, message):
        print(f"{self.lexical_analyzer.filename}:{self.token.line_number}: {Colored('error:').red()} {message}");
        print(f"Compilation {Colored('failed').red()}");
        raise Exception;

    def get_token(self):
        self.token = self.lexical_analyzer.next_token();
        return self.token;

    def undo_token(self):
        self.token = self.lexical_analyzer.prev_token();
        return self.token;

    def analyze_syntax(self):
        self.program();
        print(f"Compilation {Colored('successful').green()}");
    
    def __init__(self, filename):
        self.lexical_analyzer = Lexer(filename);
        self.qlist = QuadList();
        self.temp = TempVarSet();
        self.token = None;
        self.analyze_syntax();

    def program(self):
        if self.get_token().recognized_string == "program":
            if self.get_token().family == "id":
                progname = self.token.recognized_string;
                self.block(progname);

                if self.get_token().recognized_string == ".":
                    if self.get_token().recognized_string != "eof":
                        self.error("no characters are allowed after the fullstop indicating the end of the program");
                else:
                    self.error("every program should end with a fullstop, fullstop at the end is missing");
            else:
                if self.token.recognized_string == "eof":
                    self.error(f"name of program expected after the keyword `program`.  No program name given");
                else:
                    self.error(f"name of program expected after the keyword `program`.  Illegal program name `{self.token.recognized_string}` used");
        else:
            self.error(f"keyword `program` expected.  Expected keyword `program`, instead got `{self.token.recognized_string}`");
        self.qlist.gen_quad("halt", "_", "_", "_");
        self.qlist.gen_quad("end_block", progname, "_", "_");

    def block(self, progname):
        if self.get_token().recognized_string == "{":
            self.declarations();
            self.subprograms();
            # TODO Maybe can extract syntax
            self.qlist.gen_quad("begin_block", progname, "_", "_");
            self.blockstatements();

            if self.get_token().recognized_string != "}":
                self.error("expected closing bracket `}` after block");
        else:
            self.error("expected opening bracket `{` before block");

    def declarations(self):
        if self.get_token().recognized_string == "declare":
            self.varlist();

            if self.get_token().recognized_string != ";":
                self.error("expected declaration to end with `;`");
            self.declarations();
        else:
            self.token = self.undo_token();

    def varlist(self):
        if self.get_token().family == "id":
            self.temp.varlist.append(self.token.recognized_string);
            if self.get_token().recognized_string == ",":
                self.varlist();
            elif self.token.family == "id":
                self.error("multiple id's should be declared using commas `,`");
            else:
                self.token = self.undo_token();
        else:
            self.error(f"can only declare identifiers, instead got `{self.token.family}`");

    def subprograms(self):
        self.token = self.get_token();
        if self.token.recognized_string == "function" or self.token.recognized_string == "procedure":
            self.subprogram();
            self.subprograms();
        else:
            self.token = self.undo_token();

    def subprogram(self):
        if self.get_token().family == "id":
            subprogname = self.token.recognized_string;
            if self.get_token().recognized_string == "(":
                self.formalparlist();

                if self.get_token().recognized_string == ")":
                    self.block(subprogname);
                else:
                    self.error("expected closing parenthesis");
            else:
                self.error("expected opening parenthesis after subprogram id");
        else:
            self.error("expected id after subprogram");
        self.qlist.gen_quad("end_block", subprogname, "_", "_");

    def formalparlist(self):
        self.formalparitem();
        if self.get_token().recognized_string == ",":
            self.formalparlist();
        else:
            self.token = self.undo_token();

    def formalparitem(self):
        if self.get_token().recognized_string == "in" or self.token.recognized_string == "inout":
            if self.get_token().family != "id":
                self.error("expected id after `in` or `inout` keyword");
        elif self.token.recognized_string == ")":
            self.token = self.undo_token();
        else:
            self.error("expected `in` or `inout` keyword.  Subprogram parameters are defined using `in` or `inout`");

    # TODO Test for multiple statements on statements rule
    def statements(self):
        self.statement();
        if self.get_token().recognized_string == ";":
            pass; # TODO Code generation
        elif self.token.recognized_string == "{":
            self.statement();
            self.blockstatements();

            if self.get_token().recognized_string != "}":
                self.error("expected closing bracket `}`");
        else:
            self.error(f"expected `;` after statement instead got `{self.token.recognized_string}`");

    def blockstatements(self):
        self.statement();
        if self.get_token().recognized_string == ";":
            self.blockstatements();
        elif self.token.recognized_string == "}":
            self.token = self.undo_token();
        else:
            self.error(f"expected `;` after blockstatement instead got `{self.token.recognized_string}`");

    def statement(self):
        # TODO Parser is forward looking for terminals on statements
        # so rules called later will not have to check for initial terminal
        # that starts them.  (maybe wrong).  Possible solution is to backtrack
        # by undoing last token when moving to a subrule, then parsing them
        # again in their respective subrules (ifStat to be parsing 'if' again)
        # TODO Can implement token peeking instead of consuming only
        statement_token = self.get_token();
        self.undo_token();

        if statement_token.family == "id":
            self.assignStat();
        elif statement_token.recognized_string == "if":
            self.ifStat();
        elif statement_token.recognized_string == "while":
            self.whileStat();
        elif statement_token.recognized_string == "switchcase":
            self.switchcaseStat();
        elif statement_token.recognized_string == "forcase":
            self.forcaseStat();
        elif statement_token.recognized_string == "incase":
            self.incaseStat();
        elif statement_token.recognized_string == "return":
            self.returnStat();
        elif statement_token.recognized_string == "call":
            self.callStat();
        elif statement_token.recognized_string == "print":
            self.printStat();
        elif statement_token.recognized_string == "input":
            self.inputStat();

    def assignStat(self):
        if self.get_token().family == "id":
            assigned_value = self.token.recognized_string;
            if self.get_token().recognized_string == ":=":
                assign_expr = self.expression();
        self.qlist.gen_quad(":=", assign_expr, "_", assigned_value);

    def ifStat(self):
        if self.get_token().recognized_string == "if":
            if self.get_token().recognized_string == "(":
                condlist = self.condition();
                self.qlist.gen_quad("jump", "_", "_", "_");
                condlist.backpatch(self.qlist.next_quad());

                if self.get_token().recognized_string == ")":
                    self.statements();
                else:
                    self.error("expected closing parenthesis after an if condition");

                self.elsepart();
                # TODO backpatch
            else:
                self.error("expected opening parenthesis after if statement");

    def condition(self):
        condlist = self.boolterm();

        if self.get_token().recognized_string == "or":
            self.condition();
        else:
            self.token = self.undo_token();

        condlist.backpatch(self.qlist.next_quad());
        return condlist;

    def boolterm(self):
        condlist = self.boolfactor(LabelList());

        if self.get_token().recognized_string == "and":
            self.qlist.gen_quad("jump", "_", "_", "_");
            self.boolterm();
            # condlist.backpatch(self.qlist.next_quad());
        else:
            self.token = self.undo_token();
        
        return condlist;

    def boolfactor(self, condlist):
        if self.get_token().recognized_string == "not":
            if self.get_token().recognized_string == "[":
                self.condition();

                if self.get_token().recognized_string != "]":
                    self.error("expected closing bracket `]` after negative condition");
            else:
                self.error("expected opening bracket `[` after `not`");
        elif self.token.recognized_string == "[":
            self.condition();

            if self.get_token().recognized_string != "]":
                self.error("expected closing bracket `]` after condition");
        else:
            self.token = self.undo_token();
            first_factor = self.expression();

            if terminal_match(REL_OP, self.get_token().recognized_string):
                operator = self.token.recognized_string;
                second_factor = self.expression();
                condlist = condlist.merge(LabelList(self.qlist.next_quad()));
                self.qlist.gen_quad(operator, first_factor, second_factor, "_");
                return condlist;
            else:
                self.error("expected relational operator when comparing expressions");

    def elsepart(self):
        if self.get_token().recognized_string == "else":
            self.statements();
        else:
            self.token = self.undo_token();

    def whileStat(self):
        if self.get_token().recognized_string == "while":
            if self.get_token().recognized_string == "(":
                self.condition();

                if self.get_token().recognized_string == ")":
                    self.statements();
                else:
                    self.error("expected closing parenthesis after while statement");
            else:
                self.error("expected opening parenthesis before while statement");

    def switchcaseStat(self):
        if self.get_token().recognized_string == "switchcase":
            self.caselist();

            if self.get_token().recognized_string == "default":
                self.statements();
            else:
                self.error("expected `default` on switchcase");

    def caselist(self):
        if self.get_token().recognized_string == "case":
            self.token = self.undo_token();
            self.caseStat();
            self.caselist();
        else:
            self.token = self.undo_token();

    def caseStat(self):
        if self.get_token().recognized_string == "case":
            if self.get_token().recognized_string == "(":
                self.condition();

                if self.get_token().recognized_string == ")":
                    self.statements();
                else:
                    self.error("expected closing parenthesis after case statement");
            else:
                self.error("expected opening parenthesis before case statement");

    def forcaseStat(self):
        if self.get_token().recognized_string == "forcase":
            self.caselist();

            if self.get_token().recognized_string == "default":
                self.statements();
            else:
                self.error("expected `default` on forcase");

    def incaseStat(self):
        if self.get_token().recognized_string == "incase":
            self.caselist();

    def returnStat(self):
        if self.get_token().recognized_string == "return":
            if self.get_token().recognized_string == "(":
                retvalue = self.expression();

                if self.get_token().recognized_string != ")":
                    self.error("expected closing parenthesis after return statement");
            else:
                self.error("expected opening parenthesis on return statement");
        self.qlist.gen_quad("retv", retvalue, "_", "_");

    def callStat(self):
        if self.get_token().recognized_string == "call":
            if self.get_token().family == "id":
                proc = self.token.recognized_string;
                if self.get_token().recognized_string == "(":
                    self.actualparlist([]);

                    if self.get_token().recognized_string != ")":
                        self.error("expected closing parenthesis after call statement");
                else:
                    self.error("expected opening parenthesis on call statement");
            else:
                self.error("expected an identifier after `call` keyword");
        self.qlist.gen_quad("call", "_", "_", proc);

    def printStat(self):
        if self.get_token().recognized_string == "print":
            if self.get_token().recognized_string == "(":
                print_expr = self.expression();

                if self.get_token().recognized_string != ")":
                    self.error("expected closing parenthesis after print statement");
            else:
                self.error("expected opening parenthesis on print statement");
        self.qlist.gen_quad("out", print_expr, "_", "_");

    def inputStat(self):
        if self.get_token().recognized_string == "input":
            if self.get_token().recognized_string == "(":
                if self.get_token().family == "id":
                    input_token = self.token.recognized_string;

                    if self.get_token().recognized_string != ")":
                        self.error("expected closing parenthesis after input statement");
                else:
                    self.error("expected an identifier as a parameter to an input statement");
            else:
                self.error("expected opening parenthesis on input statement");
        self.qlist.gen_quad("inp", input_token, "_", "_");

    def expression(self):
        return self.optionalSign() + self.term();

    def optionalSign(self):
        if terminal_match(ADD_OP, self.get_token().recognized_string):
            return self.token.recognized_string;
        else:
            self.token = self.undo_token();
            return "";

    def term(self):
        factor = self.factor();

        if factor:
            addlist = self.addtermlist(factor);
        else:
            addlist = self.addtermlist(self.token.recognized_string);

        if addlist:
            return addlist;
        elif factor:
            return factor;

    def factor(self):
        if terminal_match(INTEGER, self.get_token().recognized_string):
            return self.token.recognized_string;
        elif self.token.recognized_string == "(":
            self.expression();

            if self.get_token().recognized_string != ")":
                self.error("missing parenthesis on factor expression");

            return str(self.temp);
        elif self.token.family == "id":
            current_token = self.token.recognized_string;
            if self.idtail(self.token.recognized_string):
                return str(self.temp);
            return current_token;

        # TODO Prob not necessary
        else:
            self.token = self.undo_token();
            return None;

    def idtail(self, proc):
        if self.get_token().recognized_string == "(":
            self.actualparlist([]);
            retvalue_temp = str(self.temp.new_temp());
            self.qlist.gen_quad("par", retvalue_temp, "RET", "_");
            self.qlist.gen_quad("call", "_", "_", proc);

            if self.get_token().recognized_string != ")":
                self.error("missing closing parenthesis on idtail");
            return True;
        else:
            self.token = self.undo_token();
            return False;

    def actualparlist(self, parlist):
        parresult = self.actualparitem();
        if parresult != None:
            value_expr, type = parresult;
            parlist.append((value_expr, type));

        if self.get_token().recognized_string == ",":
            self.actualparlist(parlist);
        else:
            self.token = self.undo_token();

        for item in parlist:
            self.qlist.gen_quad("par", item[0], item[1], "_");
            parlist.remove(item);

    def actualparitem(self):
        if self.get_token().recognized_string == "in":
            return self.expression(), "CV";
        elif self.token.recognized_string == "inout":
            if self.get_token().family != "id":
                self.error("expected identifier after `inout` keyword");
            return self.token.recognized_string, "REF";
        elif self.token.recognized_string == ")":
            self.token = self.undo_token();
        else:
            self.error("expected `in` or `inout` keyword.  Actual parameters are defined with `in` or `inout`");

    def multermlist(self, first_factor):
        if terminal_match(MUL_OP, self.get_token().recognized_string):
            operator = self.token.recognized_string;
            second_factor = self.factor();
            result = str(self.temp.new_temp());

            self.qlist.gen_quad(operator, first_factor, second_factor, result);
            self.multermlist(result);
        else:
            self.token = self.undo_token();

    def addtermlist(self, first_term):
        self.multermlist(self.token.recognized_string);

        if terminal_match(ADD_OP, self.get_token().recognized_string):
            operator = self.token.recognized_string;
            second_term = self.term();
            result = str(self.temp.new_temp());
            
            self.qlist.gen_quad(operator, first_term, second_term, result);
            self.addtermlist(result);
            return result;
        else:
            self.token = self.undo_token();
            return None;
    
    def generate_machine_code(self, filepath):
        print(f"machine code at `{filepath}`");
        with open(filepath, "w") as file:
            pass;

class IntermediateCode:
    def __init__(self, qlist, temp):
        # TODO Refactor (too invasive)
        self.varlist = temp.varlist;
        self.qlist = qlist;
    
    def generate_intermediate(self, filepath):
        with open(filepath, "w") as file:
            for item in self.qlist.list:
                file.write(f"{self.qlist.list[item]}\n");
    
    def generate_c_code(self, filepath):
        def write_saved_variables(varlist):
            variables = "int ";
            for i in range(len(varlist) - 1):
                variables += varlist[i] + ", ";
            variables += varlist[-1] + ";";
            file.write(f"\t{variables}\n\n");

        with open(filepath, "w") as file:
            file.write("#include <stdio.h>\n\n");
            file.write("int main(void) {\n");

            write_saved_variables(self.varlist);

            for item in self.qlist.list:
                value = self.qlist.list[item];
                if(value.operator == "begin_block"):
                    file.write(f"\tL_{value.label}:; // ({value})\n");
                elif(value.operator == "end_block"):
                    file.write(f"\tL_{value.label}:; // ({value})\n");
                elif(value.operator == ":="):
                    file.write(f"\tL_{value.label}: {value.operand3} = {value.operand1}; // ({value})\n");
                elif(terminal_match(ADD_OP, value.operator) or terminal_match(MUL_OP, value.operator)):
                    file.write(f"\tL_{value.label}: {value.operand3} = {value.operand1} {value.operator} {value.operand2}; // ({value})\n");
                elif(terminal_match(REL_OP, value.operator)):                    
                    if(value.operator == "="):
                        file.write(f"\tL_{value.label}: if({value.operand1} == {value.operand2}) goto L_{value.operand3}; // ({value})\n");
                    elif(value.operator == "<>"):
                        file.write(f"\tL_{value.label}: if({value.operand1} != {value.operand2}) goto L_{value.operand3}; // ({value})\n");
                    else:
                        file.write(f"\tL_{value.label}: if({value.operand1} {value.operator} {value.operand2}) goto L_{value.operand3}; // ({value})\n");
                elif(value.operator == "retv"):
                    file.write(f"\tL_{value.label}: return({value.operand1}); // ({value})\n");
                elif(value.operator == "jump"):
                    file.write(f"\tL_{value.label}: goto L_{value.operand3}; // ({value})\n");
                elif(value.operator == "inp"):
                    file.write(f"\tL_{value.label}: scanf(\"%d\", &{value.operand1}); // ({value})\n");
                elif(value.operator == "out"):
                    file.write(f"\tL_{value.label}: printf(\"%d\\n\", {value.operand1}); // ({value})\n");
                else:
                    pass;

            file.write("}\n");

class Entity:
    def __init__(self, name, type):
        self.name = name;
        self.type = type;

class VarEntity(Entity):
    def _init_(self, name, type, offset):
        self.type = type;
        super().__init__(name, "Variable");
        self.offset = offset;

class Function(Entity):
    def __init__(self, name, start=-1):
        super().__init__(name, "Function")
        self.start = start;
        self.arguments_list = list();
        self.framelength = -1;

class Const(Entity):
    def __init__(self, name, value):
        super().__init__(name, "Constant");
        self.value = value;

class Parameter(Entity):
    def __init__(self, name, parameter_mode, offset=-1):
        super().__init__(name, "Parameter");
        self.parameter_mode = parameter_mode;
        self.offset = offset;

class TempVariable(Entity):
    def __init__(self, name, offset=-1):
        super().__init__(name, "Tempvar");
        self.offset = offset;

class Scope:
    def __init__(self, nesting=0, enclosing_scope=None):
        self.entity_list = list();
        self.nesting = nesting;
        self.current_offset = 12;
        self.enclosing_scope = enclosing_scope;

    def add_entity(self, Entity):
        self.entity_list.append(Entity);

    def advance_current_offset(self):
        current = self.current_offset;
        self.current_offset += 4;
        return current;

class Argument:
    def __init__(self, parameter_mode, next_arg=None):
        self.parameter_mode = parameter_mode;
        self.next_arg = next_arg;

def main():
    def get_commandline_arguments():
        opt = optparse.OptionParser("Usage: python3 cimple.py <input file> [Options]");
        opt.add_option("-o", "--output", dest = "filepath", type = "string", help = "specify compilation output name");
        (options, args) = opt.parse_args();
        if(options.filepath):
            return (options.filepath, args);
        else:
            return ("a.out", args);

    def check_for_valid_compilation(args):
        if not args:
            print(f"{Colored('error').red()}: no input files (-h for help)");
            print(f"Compilation terminated");
            exit(1);

        if not os.path.exists(args[0]):
            print(f"{Colored('error').red()}: no such file or directory: '{args[0]}'");
            print(f"Compilation terminated");
            exit(1);
    
    def compile(filepath, args):
        try:
            p = Parser(args[0]);
            i = IntermediateCode(p.qlist, p.temp);

            i.generate_intermediate(f"{filepath.split('.')[0]}.int");
            i.generate_c_code(f"{filepath.split('.')[0]}.c");
            p.generate_machine_code(f"{filepath}");
        except Exception:
            pass;
    
    filepath, args = get_commandline_arguments();
    check_for_valid_compilation(args);
    compile(filepath, args);

if __name__ == "__main__":
    main();
