''' dataTypes.py

This module defines the native and unique types available
for columns, those types are BOOL which can be seen as an
isomorphism with Z_{2}, INT which defines the set of integers,
REAL is the set of real numbers, with high precision arithmetic,
STRING represents a set of values of character strings, CHAR is 
a primitive type for STRING. DATE is the set of dates of the 
form yyyy-mm-dd hh:mm:ss.

Simple types are created by indicating the type among the valid
types and a terminal value od the data, if the type transmission
succeed, then it handles an internal representation, otherwise,
the data is 'NULL' and the conversion failed. Representation and
operations depends on the machine.

The general scheme of a type in BURP is to check if the argument
is valid (is in the domain of the type), if it is, the string
representation of it is the bare value, otherwise it is NULL,
semantics indicates that NULL is an unrecognized value in the 
type.

Types = [BOOL, INT, REAL, STRING, CHAR]
'''

class BOOL(object):
    ''' Represents the Boolean datatype
    Args:
        value (str): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '' and value in ['#t', '#f']:
            self.data = str(value)
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

    def __eq__(self, other):
        return self.data == other.data

class INT(object):
    ''' Represents the Integer datatype
    Args:
        value (int or str): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '' and value.isdigit():
            self.data = int(value)
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __ne__(self, other):
        return self.data != other.data

class REAL(object):
    ''' Represents the Real datatype
    Args:
        value (str or float): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '' and '.' in value:
            slices = value.split('.')
            if len(slices) == 2:
                if slices[0].isdigit() and slices[1].isdigit():
                    self.data = float(value)
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __ne__(self, other):
        return self.data != other.data

class STRING(object):    
    ''' Represents the String datatype
    Args:
        value (str): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '':
            self.data = value
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __ne__(self, other):
        return self.data != other.data

class CHAR(object):    
    ''' Represents the Char datatype
    Args:
        value (str): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '' and len(value) == 1:
            self.data = value
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

    def __eq__(self, other):
        return self.data == other.data

    def __lt__(self, other):
        return self.data < other.data

    def __le__(self, other):
        return self.data <= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __ne__(self, other):
        return self.data != other.data

def infertype(value):
    if INT(value).__str__() != 'NULL':
        return 'INTEGER'

    if REAL(value).__str__() != 'NULL':
        return 'REAL'

    if BOOL(value).__str__() != 'NULL':
        return 'BOOL'

    if CHAR(value).__str__() != 'NULL':
        return 'CHAR'

    if STRING(value).__str__() != 'NULL':
        return 'STRING' 