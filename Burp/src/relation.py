''' relation.py

This module defines the type of a relation, the main structure in
BURP. Informally, a relation can be viewed as a structure with two
parts, a heading and a body. The heading is a collection of typed 
attributes, while the body is a collection of typed tuples whose i'th
entry has the type of the i'th attribute. The body is a set, so it must
avoid duplicates, the length of the heading is the arity of a relation, 
while the length of the body is said to be the cardinality of the 
relation. 

This module also defines the semantics of BURP, that is,
the procedual abstraction of an operation in the relational algebra.
Compound operations are expressed using base operations, if optimization
is not specified.

A relation is created by indicating the typed body, and a name.
A relation must allow tuples to be inserted, and should
handle some abstraction for relational algebra operations, the supported
basic operations are:

[SELECTION, PROJECTION, UNION, DIFFERENCE, PRODUCT]

Compound operations based on the base ones are:

[JOIN, INTERSECTION, RENAMING, ASSIGNMENT]

'''

import tabulate # For display facilities
import string # For string handling
import random # Internal naming of emporal relations

# BURP native datatypes
from dataTypes import INT
from dataTypes import REAL
from dataTypes import CHAR
from dataTypes import BOOL
from dataTypes import STRING
from dataTypes import DATE

# Error messages associated with relations
import errorMessages

class Relation(object):
    ''' Represents the kernel of BURP, and provides abstractions for operations
    The internal representation is coded in order to define operations 
    originally defined an explained by Codd.
    Args:
        name (str): the name of the relation
        types ([dataType]): the types of the columns from left to right
        attributes ([str]): the names of the columns from left to right

    '''

    def __init__(self, name, types, attributes):

        # Error handling
        self.error_queue = []

        # Relation name
        self.name = name

        # Relations arity
        self.arity = len(attributes)

        # Relation heading (attribute_name, type)
        self.heading = None

        # Relation tuples internal representation, used for hashing
        self.tuples = []

        # Memory mapping of relations tuples, used for insertion on new relations
        self.data = []

        # Number of elements in the realtion
        self.cardinality = 0

        if len(types) == self.arity:
            self.heading = zip([_.upper() for _ in attributes], types)

        else:
            self.error_queue.append(errorMessages.ERROR001(self.name))

    # Modeling methods

    def insert(self, to_insert):
        ''' Handles data insertion on relations, the insertion
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
                    self.error_queue.append(errorMessages.ERROR002(self.name, str(itm.data), 
                        real_types[i].__name__, str(self.get_lazy_type(itm))))
                i += 1

            if flag:
                # Internal data representation of tuple
                real_data = [_.data for _ in to_insert]
                real_data = tuple(real_data)

                # Unique success branch
                if real_data not in self.tuples:
                    self.tuples.append(real_data)
                    self.data.append(to_insert)
                    self.cardinality += 1
                    ans = True

                else:
                    self.error_queue.append(errorMessages.ERROR003(self.name, str(real_data)))

        else:
            self.error_queue.append(errorMessages.ERROR004(self.name, str(self.arity), str(length)))

        return ans

    # Base relational algebra operations, sets operations

    def union(self, arg_relation):
        ''' Defines the union of two realtions. Mathematically, 
            the union is defined as tuples both in R1, and in R2.
            Formally, 

            R U P = {t| t in R \/ t in R}

            Both relations should be union compatible, that is, the 
            columns domains must be the same in the same order for
            both relations, in order to guarantee this property, we 
            check compatibility. Tuples in the intersection must be
            omitted.

            Args:
                arg_relation (Relation): another relation object

            Returns:
                Relation: union of this relation and the given one

        '''

        real_types = [tp for (_, tp) in self.heading] # Relation's types
        arg_types = [tp for (_, tp) in arg_relation.heading] # Other relation's types

        ans = None

        seed = string.digits 
        new_name = 'UnionOn' + self.name.lower().capitalize() 
        new_name += 'With' + arg_relation.name.lower().capitalize()
        new_name += ''.join(random.choice(seed) for _ in range(5))

        # Unique branch of success
        if real_types == arg_types:
          

            relation_attributes = [at for (at, _) in self.heading]
            other_attributes = [at for (at, _) in arg_relation.heading]

            attributes = relation_attributes

            ans = Relation(new_name, real_types, attributes) # New relation

            # Appends both tuple set

            for itm in self.data:
                ans.insert(itm)

            for itm in arg_relation.data:
                ans.insert(itm)

            self.error_queue += ans.error_queue

        else:
            r_types = [itm.__name__ for itm in real_types]
            o_types = [itm.__name__ for itm in arg_types]
            msg = errorMessages.ERROR005(new_name, str(r_types), str(o_types))
            self.error_queue.append(msg)

        return ans

    def diference(self, arg_relation):

        real_types = [tp for (_, tp) in self.heading] # Relation's types
        arg_types = [tp for (_, tp) in arg_relation.heading] # Other relation's types

        ans = None

        seed = string.digits 
        new_name = 'DifferenceOn' + self.name.lower().capitalize() 
        new_name += 'With' + arg_relation.name.lower().capitalize()
        new_name += ''.join(random.choice(seed) for _ in range(5))

        # Unique branch of success
        if real_types == arg_types:          

            relation_attributes = [at for (at, _) in self.heading]
            other_attributes = [at for (at, _) in arg_relation.heading]

            attributes = relation_attributes

            ans = Relation(new_name, real_types, attributes)

            for itm in self.data:
                if itm not in arg_relation.data:
                    ans.insert(itm)

            self.error_queue += ans.error_queue

        else:
            r_types = [itm.__name__ for itm in real_types]
            o_types = [itm.__name__ for itm in arg_types]
            msg = errorMessages.ERROR005(new_name, str(r_types), str(o_types))
            self.error_queue.append(msg)

        return ans

    def intersection(self, arg_relation):

        return self.diference(self.diference(arg_relation))

    def cross(self, arg_relation):
        ''' Handles cartesian product for the Relation datatype.
            It represents all the combinations of tuples from both
            entry relations appended in one grat table. The properties
            of the output relation are given:

            arity(R) = k1, arity(S) = k2
            R x S = {r @ s | r in R /\ s in S}
            arity(R x S) = k1 + k2
            |R x S| = |R| * |S|

            Args:
                arg_relation (Relation): the other relation to be 
                able to perform the binary operation

            Returns:
                Relation: a relation representing the cross product
                of two relations
        '''

        real_types = [tp for (_, tp) in self.heading] # Relation's types
        arg_types = [tp for (_, tp) in arg_relation.heading] # Other relation's types
        new_types = real_types + arg_types # New relation's types

        ans = None

        seed = string.digits 
        new_name = self.name.lower().capitalize() 
        new_name += 'Cross' + arg_relation.name.lower().capitalize()
        new_name += ''.join(random.choice(seed) for _ in range(5))

        relation_attributes = [self.name + '.' + at for (at, _) in self.heading]
        other_attributes = [arg_relation.name + '.' + at for (at, _) in arg_relation.heading]
        new_attributes = relation_attributes + other_attributes

        ans = Relation(new_name, new_types, new_attributes)

        for my_tuple in self.data:
            for other_tuple in arg_relation.data:
                my_tuple = list(my_tuple)
                other_tuple = list(other_tuple)
                final_tuple = my_tuple + other_tuple
                ans.insert(final_tuple)

        return ans

    # Relational operators

    def project(self, attributes):
        ''' Handles projection operation as in relation algebra.
            it discriminate certain columns of the relation to 
            create a new relation with the original data but just
            with the indicated columns. It should check pertinence
            of execution as well as new relation creation.

            Args:
                attributes (list): attributes to project

            Returns:
                Relation: the projected relation on the original one

        '''

        ans = None # Final relation
        attributes = [_.upper() for _ in attributes] # Internal representation
        relation_attributes = [at for (at, _) in self.heading] # Relation's attributes

        indexes = [] # Indexes of the received attributes in the relation's attributes

        flag = True
        
        for attribute in attributes:
            # Pertinence of execution
            if attribute not in relation_attributes:
                flag = False
                self.error_queue.append(errorMessages.ERRO6006(attribute, self.name))
            if flag:
                position = relation_attributes.index(attribute)
                indexes.append(position)

        if flag:

            # New relation's name
            seed = string.digits
            new_name = 'ProjectionOn' 
            new_name += self.name.lower().capitalize() + '-' 
            new_name += ''.join(random.choice(seed) for _ in range(5))

            # New relation's types
            real_types = [tp for (_, tp) in self.heading]
            new_types = [real_types[i] for i in indexes]

            # New relation's attributes
            real_attributes = [at for (at, _) in self.heading]
            new_attributes = [real_attributes[i] for i in indexes]

            # Return value creation
            ans = Relation(new_name, new_types, new_attributes)

            # Return value population
            for itm in self.data:
                addition_tuple = [itm[i] for i in indexes]
                ans.insert(addition_tuple)

            self.error_queue += ans.error_queue

        return ans

    def select(self, columns, rel_ops, values, connectors):
        pass

    # Compound relational algebra operations

    def join(self, arg_relation):
        pass

    # Auxiliary functions

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

    def flush(self):
        self.error_queue = []

    def rename(self, new_name):
        self.name = new_name

    # I/O methods for BURP internal implementation

    def display(self):
        ''' Display the relation in tabular form, that is, whith the named columns
            and data

            references:
                [1]. http://jtauber.com/blog/2005/11/11/relational_python:_displaying_relations/
                [2]. https://pypi.python.org/pypi/tabulate
                [3]. https://bitbucket.org/astanin/python-tabulate
                
        '''

        headers = [at for (at, _) in self.heading]
        table = []
        for tpl in self.tuples:
            new_tpl = []
            for itm in tpl:
                new_tpl.append(str(itm))
            table.append(new_tpl)

        print tabulate.tabulate(table, headers, tablefmt="grid")