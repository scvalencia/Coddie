''' relation.py

This module defines the class of a relation, the main structure in
BURP. Informally, a relation can be viewed as a structure with two
parts, a heading and a body. The heading is a collection of typed 
attributes, while the body is a collection of typed tuples whose i'th
entry has the type of the i'th attribute. The body is a set, so it must
avoid duplicates, the length of the hading is the arity of a relation, 
while the length of the body is said to be the cardinality of the 
relation. This module also defines the semantics of BURP, that is,
the procedual abstraction of an operation in the relational algebra.
Compound operatons are expressed using base operations, if optimization
is not specified.

A relation is created by indicating the typed body, and a name.
A relation must allow tuples to be inserted, and should
handle some abstraction for relational algebra operations, the supported
basic operations are:

[SELECTION, PROJECTION, UNION, DIFFERENCE, CARTESIAN-PRODUCT]

Compound operations based on the base ones are:

[JOIN, INTERSECTION, RENAMING, ASSIGNMENT]

'''

import tabulate

from dataTypes import INT
from dataTypes import REAL
from dataTypes import CHAR
from dataTypes import BOOL
from dataTypes import STRING
from dataTypes import DATE

class Relation(object):
    ''' Represents the kernel of BURP, and provides abstractions for operations
    Args:
        name (str): the name of the relation
        types (dataType): the types of the columns from left to right
        attributes (str): the names of the columns from left to right

    '''

    def __init__(self, name, types, attributes):
        ''' Internal representation of a relation described as in Codd,
            is done using sets, and dictionaries.
        '''
        self.error_queue = [] # Error handling
        self.name = name
        self.arity = len(attributes)
        self.heading = None
        self.tuples = []
        self.cardinality = 0

        if len(types) == self.arity:
            self.heading = zip(attributes, types)
        else:
            self.error_queue.append("The length of types must be the same length of attributes")

    # Modeling methods

    def insert(self, to_insert):
        ''' Handles data insertion on a relations, the insertion
            is successful iff the object is not already in the body
            and the desired types are the relation types defined
            in self.types. If the insertion failed, related information
            shall be included in the respective error_queue.

        Args:
            to_insert (list): the new row in the relation

        Returns:
            bool: True if successful, False otherwise
        '''

        ans = False # Success control
        length = len(to_insert) 
        if length == self.arity:
            flag = True
            real_types = [tp for (_, tp) in self.heading] # Types of the relation

            i = 0
            for itm in to_insert:
                if not isinstance(itm, real_types[i]):
                    flag = False
                    error_message = "Error inserting " + str(itm.data) + ". "
                    error_message += "Expected type is: " + real_types[i].__name__
                    error_message += ". Received type is " + self.get_lazy_type(itm)
                    self.error_queue.append(error_message)
                i += 1

            if flag:
                # Internal data representation of tuple
                real_data = [_.data for _ in to_insert]
                real_data = tuple(real_data)

                # Unique success branch
                if real_data not in self.tuples:
                    self.tuples.append(real_data)
                    self.cardinality += 1
                    ans = True
                    
                else:
                    error_message = str(real_data) + " is already present on the relation."
                    self.error_queue.append(error_message)

        else:
            error_message = "Length of the tuple must be the same of the columns. "
            error_message += "Expected value: " + str(self.arity)
            error_message += ". Received value: " + str(length)
            self.error_queue.append(error_message)

        return ans

    # Base relational algebra operations

    def project(self, attributes):
        pass

    def select(self, columns, rel_ops, values, connectors):
        pass

    def union(self, arg_relation):
        pass

    def cross(self, arg_relation):
        pass

    def doference(self, arg_relation):
        pass

    # Compound relational algebra operations

    # Internal data handling methods

    def get_lazy_type(self, value):
        if BOOL(value).data != '':
            return 'BOOL'
        elif INT(value).data != '':
            return 'INT'
        elif REAL(value).data != '':
            return 'REAL'
        elif STRING(value).data != '':
            return 'STRING'
        elif CHAR(value).data != '':
            return 'CHAR'
        elif DATE(value).data != '':
            return 'DATE'
        else:
            return 'CONST'

    # I/O methods for BURP internal implementation

    def display(self):
        ''' Display the relation in tabular form, that is, whith the named columns
            and data

            references:
                [1]. http://jtauber.com/blog/2005/11/11/relational_python:_displaying_relations/
                [2]. https://pypi.python.org/pypi/tabulate
                [3]. https://bitbucket.org/astanin/python-tabulate
                
        '''

        pass


r = Relation('S', [INT, INT, STRING], ['ID', 'QTY', 'NAME'])
print r.insert([INT(1), INT(2), STRING("Hola")])
print r.insert([INT(1), INT(2), STRING("Hola")])
print r.tuples
print r.error_queue