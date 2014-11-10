import tabulate
import Burp.dbTypes.dbTypes as dbTypes


class Relation:
    def __init__(self, types, attributes, restrictions, keys):
        self.error_queue = []
        if len(types) == len(attributes):
            self.types = types
            self.attributes = attributes
            self.restrictions = restrictions
            self.tuples = []
            self.keys = keys
        else:
            self.error_queue.append('The length of types must be the same \
                                    length of attributes')


    def add_tuple(self, tuple_):
        length = len(tuple_)
        flag = True
        if length == len(self.attributes):

            for i in range(length):
                item = tuple_[i]
                type_of = self.types[i]
                restriction = self.restrictions[i]
                if not isinstance(item, type_of):
                    flag = False
                    break
                if restriction:
                    if not restriction(item):
                        flag = False
                        break

            if flag:
                if tuple_ not in self.tuples:
                    self.tuples.append(tuple_)
            pass
        return flag

    def destroy(self):
        self.error_queue = []
        self.types = []
        self.attributes = []
        self.restrictions = []
        self.tuples = []
        self.keys = []


    def __str__(self):
        headers = self.attributes
        table = []
        for tpl in self.tuples:
            new_tpl = []
            for itm in tpl:
                new_tpl.append(str(itm))
            table.append(new_tpl)

        return tabulate.tabulate(table, headers, tablefmt="grid")


attributes = ['ID', 'Name', 'IsCool']
types = [dbTypes.INT, dbTypes.STRING, dbTypes.BOOL]
restrictions = [None, lambda a : len(str(a)) > 4, None]
tuple_1 = [dbTypes.INT('1'), dbTypes.STRING('Bages'), dbTypes.BOOL('TRUE')]
tuple_2 = [dbTypes.INT('2'), dbTypes.STRING('Valencia'), dbTypes.BOOL('FALSE')]
tuple_3 = [dbTypes.INT('3'), dbTypes.STRING('Florez'), dbTypes.BOOL('FALSE')]
tuple_4 = [dbTypes.INT('2'), dbTypes.STRING('Valencia'), dbTypes.BOOL('FALSE')]

rel = Relation(types, attributes, restrictions, [])
rel.add_tuple(tuple_1)
rel.add_tuple(tuple_2)
rel.add_tuple(tuple_3)
rel.add_tuple(tuple_4)
print rel

