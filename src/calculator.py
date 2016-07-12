import datatypes

def _prefix2infix(expression):
    infix = ''
    operand = expression[0]

    equivalent = {'=' : '==', '<>' : '!='}

    if operand in ['and', 'or']:
        infix += '('
        for itm in expression[1:-1]:
            infix += _prefix2infix(itm)
            infix += ' ' + operand + ' '
        infix += _prefix2infix(expression[-1])
        infix += ')'

    if operand in ['=', '<=', '>=', '<>', '<', '>']:
        attribute = expression[1]
        value_or_attribute = expression[2]
        infix += '(%s %s %s)' % \
            (attribute, equivalent[operand] if operand in equivalent else operand, \
                value_or_attribute)

    if operand == 'not':
        attribute = expression[1]
        infix += '(not %s)' % attribute

    return infix

lst1 = ['and', ['=', 'name', '"Pepito"'], ['<=', 'age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"']]]
print _prefix2infix(lst1)[1:-1]
print
lst2 = ['and', ['not', 'married'], ['=', 'name', '"Julian"'], ['=', 'cruxified', '#t']]
print _prefix2infix(lst2)[1:-1]
lst3 = ['and', ['=', 'name', '"Pepito"'], ['<=', 'age', '45'], ['or', ['=', 'religion', '"muslim"'], ['<>', 'lastname', '"Curry"'], ['and', ['not', 'married'], ['=', 'name', '"Julian"'], ['=', 'cruxified', '#t']]]]
print _prefix2infix(lst3)[1:-1]