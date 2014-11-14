import tabulate
import dataTypes


class Relation(object):

    def __init__(self, name, types, attributes, key):
        self.error_queue = []
        if len(types) == len(attributes):
            self.name = name
            self.types = types
            self.attributes = attributes
            self.tuples = []
            self.used_keys = []
            self.key_attribute = key
        else:
            self.error_queue.append('The length of types must be the same length of attributes')

    def insert(self, register, aux = False):
        ans = False
        length = len(register)
        if not aux:
            if length == len(self.attributes):
                table = dict(zip(self.attributes, map(str, register)))
                if table[self.key_attribute] in self.used_keys:
                    self.error_queue.append('Primary key violated: ' + table[self.key_attribute] + ' inserting ' + str(map(str, register)))
                else:                
                    flag = True
                    for i in range(length):
                        obj = register[i]
                        type_obj = self.types[i]
                        if isinstance(obj, type_obj):
                            pass
                        else:
                            self.error_queue.append('Type constraint violated inserting ' + str(map(str, register)) + '. Expected type is: ' + str(type_obj))
                            flag = False
                            break
                    if flag:
                        self.used_keys.append(table[self.key_attribute])
                        self.tuples.append(register)
                    ans = flag
        else:
            flag = True
            for i in range(length):
                obj = register[i]
                type_obj = self.types[i]
                if isinstance(obj, type_obj): pass
                else:
                    self.error_queue.append('Type constraint violated inserting ' + str(map(str, register)) + '. Expected type is: ' + str(type_obj))
                    flag = False
                    break
            if flag:
                table = dict(zip(self.attributes, map(str, register)))
                self.tuples.append(register)
            ans = flag
        return ans

    def delete(self, pk):
        pk = str(pk)
        ans = True
        if pk not in self.used_keys:
            self.error_queue.append(str(pk) + ' not found in table.' )
            ans = False
        else:
            index = self.attributes.index(self.key_attribute)
            tuples = []
            for item in self.tuples:
                obj = []
                for itm in item:
                    obj.append(str(itm))
                obj = tuple(obj)
                tuples.append(obj)

            obj = filter(lambda x : x[self.attributes.index(self.key_attribute)] == pk, tuples)
            obj = obj.pop(0)
            index_object = tuples.index(obj)
            self.used_keys.pop(index_object)
            self.tuples.pop(index_object)

    def project(self, attributes):
        length = len(filter(lambda x : x in self.attributes, attributes))
        if length == len(attributes):
            indeces = [self.attributes.index(_) for _ in attributes]
            types = [self.types[i] for i in map(int, indeces)]
            type_names = map(str, types)
            name = 'ProjectionOn' + self.name.capitalize()
            new_relation = Relation(name, types, attributes, None)
            for itm in self.tuples:
                to_add = [itm[_] for _ in map(int, indeces)]
                new_relation.insert(to_add, True)            
            return new_relation
        else:
            self.error_queue.append('Attribute not in table, unable to perform projection.')

    def selection(self, arguments, rel_ops, values, connectors):
        # Shouldn't contain NOT, those should be processed earlier
        if len(arguments) == len(rel_ops) == len(values):
            if True: 
                types = dict(zip(self.attributes, self.types))
                ans = Relation('SelectionOn' + self.name, self.types, self.attributes, self.key_attribute)
                args_types = [types[_] for _ in arguments]
                positions = map(lambda x : self.attributes.index(x) , arguments)
                relations = zip(positions, rel_ops, values)
                if args_types == [self.types[int(_)] for _ in positions]:
                    variables_of_comparisson = self.get_variable_comparisson_values(values)
                    if variables_of_comparisson == []:
                        i = 0
                        for itm in self.tuples:
                            if self.compose_filter(i, relations, connectors):
                                ans.insert(itm)
                            i += 1
                    else:
                        i = 0
                        relations = self.replace_values_by_index(relations)
                        for itm in self.tuples:
                            if self.compose_filter(i, relations, connectors, False, variables_of_comparisson):
                                ans.insert(itm)
                            i += 1                    
                else:
                    self.error_queue.append('Wrong types in selection statement')
                # Check types and so on, if argument
                return ans
        else:
            self.error_queue.append('Malformed predicate')

    def replace_values_by_index(self, relations):
        positions, rel_ops, values = zip(*relations)
        common = set(self.attributes).intersection(set(values))
        values = [self.attributes.index(_) if (_ in common) else (_, False) for _ in values]
        return zip(positions, rel_ops, values)

    def compose_filter(self, position, relations, connectors, normal_form = True, indexes = None):
        connectors_copy = [_ for _ in connectors]
        if normal_form:
            ans = True
            if connectors_copy[0] == 'AND':
                ans = True
            else:
                ans = False
            while True:
                if connectors_copy == []:
                    break
                operation = self.map_relational_operator(connectors_copy.pop(0))
                for itm in relations:
                    left = self.tuples[position][int(itm[0])].data
                    rigth = itm[2]
                    value = self.relation_operation(itm[1], left, rigth)
                    ans = operation(ans, value)       
            return ans
        else:          
            ans = True
            if connectors_copy[0] == 'AND':
                ans = True
            else:
                ans = False
            while True:
                if connectors_copy == []:
                    break
                operation = self.map_relational_operator(connectors_copy.pop(0))
                for itm in relations:
                    left = self.tuples[position][int(itm[0])].data
                    rigth = itm[2]
                    if isinstance(rigth, tuple):
                        rigth = rigth[0]
                    else:
                        rigth = self.tuples[position][int(itm[2])].data
                    value = self.relation_operation(itm[1], left, rigth)
                    ans = operation(ans, value)       
            return ans

    def map_relational_operator(self, value):
        if value == 'AND':
            return lambda a, b : a and b
        elif value == 'OR':
            return lambda a, b : a or b

    def relation_operation(self, rel_op, a, b):
        if rel_op == '=':
            return a == b
        elif rel_op == '<>':
            return a != b
        elif rel_op == '<':
            return a < b
        elif rel_op == '>':
            return a > b
        elif rel_op == '<=':
            return a <= b
        elif rel_op == '>=':
            return a >= b

    def get_lazy_type(self, value):
        if dataTypes.BOOL(value).data != '':
            return 'BOOL'
        elif dataTypes.INT(value).data != '':
            return 'INT'
        elif dataTypes.REAL(value).data != '':
            return 'REAL'
        elif dataTypes.STRING(value).data != '':
            return 'STRING'
        elif dataTypes.CHAR(value).data != '':
            return 'CHAR'
        elif dataTypes.DATE(value).data != '':
            return 'DATE'
        else:
            return 'CONST'

    def get_variable_comparisson_values(self, values):
        ans = []
        i = 0
        common = set(self.attributes).intersection(set(values))
        ans = [(self.attributes.index(_), values.index(_)) for _ in common]
        return ans

    def __str__(self):
        headers = self.attributes
        table = []
        for tpl in self.tuples:
            new_tpl = []
            for itm in tpl:
                new_tpl.append(str(itm))
            table.append(new_tpl)

        return tabulate.tabulate(table, headers, tablefmt="grid")

'''
attributes = ['ID', 'NAME', 'IS_COOL']
types = [dataTypes.INT, dataTypes.STRING, dataTypes.BOOL]
key = 'ID'
tuple_1 = (dataTypes.INT(1), dataTypes.STRING('Natalia'), dataTypes.BOOL('FALSE'))
tuple_2 = (dataTypes.INT(2), dataTypes.STRING('Carlos'), dataTypes.BOOL('TRUE'))
rel = Relation('Dudes', types, attributes, key)
rel.insert(tuple_1)
rel.insert(tuple_2)
print rel
rel.delete('2')
for itm in rel.error_queue:
    print itm
print rel
tuple_2 = (dataTypes.INT(2), dataTypes.STRING('Carlos'), dataTypes.BOOL('TRUE'))
rel.insert(tuple_2)
print rel

print rel.project(['NAME'])
print rel.project(['NAME', 'ID'])


r = Relation('Projection', [dataTypes.INT], ['ID'], 'ID')
for i in range(8):
    r.insert((dataTypes.INT(i),), True)


r.insert((dataTypes.INT(19),), True)
r.insert((dataTypes.INT(19),), True)
print r
r.delete('5')
r.delete('19')
for i in r.error_queue:
    print i
print r
'''

attributes = ['NAME', 'AGE', 'WEIGHT']
types = [dataTypes.STRING, dataTypes.INT, dataTypes.INT]
tuple_1 = (dataTypes.STRING('Harry'), dataTypes.INT(34), dataTypes.INT(80))
tuple_2 = (dataTypes.STRING('Sally'), dataTypes.INT(28), dataTypes.INT(64))
tuple_3 = (dataTypes.STRING('George'), dataTypes.INT(29), dataTypes.INT(70))
tuple_4 = (dataTypes.STRING('Helena'), dataTypes.INT(54), dataTypes.INT(54))
tuple_5 = (dataTypes.STRING('Peter'), dataTypes.INT(34), dataTypes.INT(80))
rel = Relation('Persons', types, attributes, 'NAME')
rel.insert(tuple_1)
rel.insert(tuple_2)
rel.insert(tuple_3)
rel.insert(tuple_4)
rel.insert(tuple_5)
print rel
print rel.selection(['AGE', 'WEIGHT'], ['=', '='], ['WEIGHT', 'ANS'], ['OR'])

