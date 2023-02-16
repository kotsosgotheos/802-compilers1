class TempVarSet:
    def __init__(self):
        self.current = 0;
        self.list = ["T_" + str(self.current)];
    
    def new_temp(self):
        self.current += 1;
        self.list.append("T_" + str(self.current));
        return self;
    
    def __str__(self):
        return self.list[-1];

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
        return f"{self.label}: {self.operator}, {self.operand1}, {self.operand2}, {self.operand3}";

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

qlist = QuadList();
l1 = LabelList(qlist.next_quad());
qlist.gen_quad("jump", "_", "_", "_");
qlist.gen_quad("+", "a", "1", "a");
l2 = LabelList(qlist.next_quad());
qlist.gen_quad("jump", "_", "_", "_");
l = l1.merge(l2);
qlist.gen_quad("+", "a", "2", "a");
l.backpatch(qlist.next_quad());

print(qlist);
print(l);

t = TempVarSet();
print(t);
print(t.new_temp());
print(t.new_temp());
print(t.new_temp());
t.new_temp();
print(t);
