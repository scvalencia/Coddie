class Calculator:
    def __init__ (self):
        self.stack = []

    def push(self, p):
        if p in ['and', 'not']:
            while self.stack:
                print self.convert(self.stack.pop())
        if p in ['=', '<=', '>=', '<>']:
            op1 = self.stack.pop()
            op2 = self.stack.pop()
            self.stack.append ('(%s %s %s)' % (op1, p, op2) )
        elif p == '!':
            op = self.stack.pop()
            self.stack.append ('%s!' % (op) )
        else:
            self.stack.append(p)

    def convert (self, l):
        if isinstance(l, str):
            return l
        l.reverse ()
        for e in l:
            self.push (e)
        return self.stack.pop ()

c = Calculator ()

def _prefix2infix(expression):
    infix = ''
    operand = expression[0]

    if operand in ['and', 'or']:
        infix += '('
        for itm in expression[1:-1]:
            infix += _prefix2infix(itm)
            infix += ' ' + operand + ' '
        infix += _prefix2infix(expression[-1])
        infix += ')'
    if operand in ['=', '<=', '>=', '<>']:
        infix += '(%s %s %s)' % \
            (expression[1], operand if operand in ['=', '<=', '>='] else '!=', \
                expression[2])
    if operand == 'not':
        infix += '(not %s)' % expression[1]

    return infix

lst1 = ['and', ['=', 'name', '"Pepito"'], ['<=', 'age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"']]]
print _prefix2infix(lst1)
print
lst2 = ['and', ['not', 'married'], ['=', 'name', '"Julian"'], ['=', 'cruxified', '#t']]
print _prefix2infix(lst2)
lst3 = ['and', ['=', 'name', '"Pepito"'], ['<=', 'age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"'], ['and', ['not', 'married'], ['=', 'name', '"Julian"'], ['=', 'cruxified', '#t']]]]
print _prefix2infix(lst3)


# print c.convert()

'''
['and', ['=', 'name', '"Pepito"'], ['<=', 'age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"']]]
['and', ['=', 'relation.name', '"Pepito"'], ['<=', 'relation.age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"']]]

(self.tuples[idx1] == "Pepito") and (self.tuples[idx2] <= 45) and ((self.tuples[idx3] == "muslim") or (self.tuples[idx4] == "Curry"))
'''

lst = [1, 2, "Hola", 5, 45.6]
a = lambda idx, val : lst[idx] == val
b = lambda idx, val : lst[idx] != val

c = lambda idx, val : a(idx, val) and b(idx, val) 