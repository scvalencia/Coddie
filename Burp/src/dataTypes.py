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

Types = [BOOL, INT, REAL, STRING, CHAR, DATE]
'''

class BOOL(object):
    ''' Represents the Boolean datatype
    Args:
        value (str): Normal form of a value of the type
    '''
    def __init__(self, value):
        value = str(value)
        if value != '' and value in ['TRUE', 'FALSE']:
            self.data = str(value)
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

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

class DATE(object):
    ''' Represents the Date datatype
    Args:
        value (str): Normal form of a value of the type, it should have the form
                     yyyy-mm-dd hh:mm:ss.
    '''

    def __init__(self, value):
        value = str(value)
        parts = value.split()
        slices = parts[0].split('-')
        hour_parse = parts[1].split(':')
        if value != '' and len(slices) == 3 and len(hour_parse) == 3:
            self.year = slices[0]
            self.month = slices[1]
            self.day = slices[2]
            self.hour = hour_parse[0]
            self.minutes = hour_parse[1]
            self.seconds = hour_parse[2]
            self.data = value
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'