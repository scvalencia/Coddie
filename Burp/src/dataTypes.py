class BOOL:
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

class INT:
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

class REAL:
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

class STRING:
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

class CHAR:
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

class DATE:
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

def test():
    true = BOOL('TRUE')
    print true
    false = BOOL('FALSE')
    print false
    one = INT(123123)
    print one
    peano = REAL(322.23423)
    print peano
    string = STRING("Sebastian Valencia")
    print string
    char = CHAR('a')
    print char
    dt = DATE('2011-09-21 15:31:54')
    print dt