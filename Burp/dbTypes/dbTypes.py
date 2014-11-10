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
            self.data = str(value)
        else:
            self.data = ''

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return 'NULL'

class DOUBLE:
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

class YEAR:
    def __init__(self, year):
        year = str(year)
        if year != '' and len(year) == 4:
            self.data = year
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
        if value != '' and ' ' not in value:
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

class TEXT:
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

class ENUM:
    v_types = ['BOOL', 'INT', 'DOUBLE', 'YEAR', 'STRING', 'CHAR', 'TEXT', 'DATE']
    def __init__(self, name, types, attributes):
        #print len(set(types)) Sjould be one!!!
        if len(types) == len(attributes) and len(set(types)) == 1:
            is_valid = len(filter(lambda a : a not in self.v_types, types)) == 0
            if is_valid:
                self.name = name
                self.data = attributes
        else:
            self.name = ''
            self.data = ''

    def is_value(self, val):
        return val in self.data

    def __str__(self):
        if self.name:
            ans = self.name + ' {\n'
            if self.data:
                for itm in self.data:
                    ans += '\t' + str(itm) + '\n'
            ans += '}'
            return ans
        else:
            return '{}'