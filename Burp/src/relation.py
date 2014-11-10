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
        if len(arguments) == len(rel_ops) == len(values):
            if len(arguments) - 1 == len(connectors): 
                types = dict(zip(self.attributes, self.types))
                args_types = [types[_] for _ in arguments]
                positions = map(lambda x : self.attributes.index(x) , arguments)
                # Check types and so on, if argument
        else:
            self.error_queue.append('Malformed predicate')

    def parse_relationl_operation(self, rel_op):
        if rel_op == '=':
            return lambda a, b : a == b
        elif rel_op == '<>':
            return lambda a, b : a != b
        elif rel_op == '<':
            return lambda a, b : a < b
        elif rel_op == '>':
            return lambda a, b : a > b
        elif rel_op == '<=':
            return lambda a, b : a <= b
        elif rel_op == '>=':
            return lambda a, b : a >= b



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

attributes = ['ID', 'NAME', 'IS_COOL']
types = [dataTypes.INT, dataTypes.STRING, dataTypes.BOOL]
tuple_1 = (dataTypes.INT(1), dataTypes.STRING('Natalia'), dataTypes.BOOL('FALSE'))
tuple_2 = (dataTypes.INT(2), dataTypes.STRING('Carlos'), dataTypes.BOOL('TRUE'))
key = 'ID'
rel = Relation('Dudes', types, attributes, key)
rel.insert(tuple_1)
rel.insert(tuple_2)
rel.selection(['NAME', 'ID'], ['=', '<>'], ['Sebastian', 13], ['AND'])
