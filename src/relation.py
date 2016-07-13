import random
import string
import tabulate
import datatypes

def _callerror(error):
	print error.replace('  ', ' ')

class Tuple(object):

	_ERROR01 = 'Unrecognized value %s on tuple %s'

	def __init__(self, data):
		self.data = data
		self.arity = len(self.data)
		self.types = map(datatypes.infertype, self.data)
		self.hash = self.__hash__()

		nullable = map(lambda x : x == 'NULL', self.types)
		if any(nullable):
			item = filter(lambda x : x[1] == 'NULL', enumerate(self.types))
			index = item.pop()[0]
			_callerror(self._ERROR01 % (str(self.data[index]), self.data))		

	def __hash__(self):
		aux = ''
		for datum in self.data:
			aux += datum

		i = 0; ans = 0
		while i < len(aux):
			ans = ans * 31 + ord(aux[i])
			i = i + 1

		return ans

	def __iter__(self):
		return self.data.__iter__()

	def __getitem__(self, i):
		return self.data[i]

class Relation(object):

	_ERROR01 = ('Error while creating relation %s. Types arity is %d, '
					'while attributes arity is %d')

	_ERROR02 = ('Error while inserting tuple into the %s relation. '
					'Relation\'s arity is %d, but receive a %d-tuple')

	_ERROR03 = ('Error while inserting tuple into the %s relation. '
					'\n\tRelation\'s type is: %s.\n\tTuple\'s type is: %s')

	_ERROR04 = ('Error while executing projection operator on %s. %s is not'
					'in the relation\'s schema')

	_ERROR05 = ('Error while executing set operator: %s. Relation %s, and '
					'relation %s, are not type-compatible')

	def __init__(self, name, types, attributes):
		if len(types) != len(attributes):
			_callerror(self._ERROR01 % (name, len(types), len(attributes)))
			return None

		self.name = name
		self.attributes = attributes
		self.types = types		
		self.schema = zip(attributes, types)
		self.arity = len(self.schema)
		self.tuples = {}
		self.cardinality = 0
		self.derivativeids = {'PROJECT' : 0}

	def insert(self, tpl):
		t = Tuple(tpl)

		if t.arity != len(self.schema):
			_callerror(self._ERROR02 % (self.name, self.arity, t.arity))
			return
		if t.types != self.types:
			_callerror(self._ERROR03 % (self.name, self.types, t.types))
			return
		if t.hash in self.tuples:
			return

		self.tuples[t.hash] = t

	def delete(self, tpl):
		t = Tuple(tpl)

		if t.hash not in self.tuples:
			return

		self.tuples.pop(t.hash)

	def project(self, arguments):

		for arg in arguments:
			if arg not in self.attributes:
				_callerror(self._ERROR04 % (self.name, arg))
				return

		idxs = map(lambda x : self.attributes.index(x), arguments)

		resulting_name = self.name + '_projection_' + self._random_string()
		resulting_type = [self.types[idx] for idx in idxs]
		resulting_relation = Relation(resulting_name, resulting_type, arguments)
		
		for tpl in self.tuples:
			lst = [self.tuples[tpl][idx] for idx in idxs]
			resulting_relation.insert(tuple(lst))

		return resulting_relation

	def _attribute_equiv(self, attribute):
		idx = self.attributes.index(attribute)
		return str(idx)

	def _attribute_value_equiv(self, attribute, value_or_attribute, iterator='tpl'):

		equiv_types = {'INTEGER' : 'int', 'REAL' : 'float'}

		isattribute = lambda x : x in self.attributes
		attribute_type = self.types[self.attributes.index(attribute)]
		attribute_equiv_template = 'self.tuples[%s].data[%s]'

		attribute_equiv = attribute_equiv_template % (iterator, self._attribute_equiv(attribute))
		value_equiv = value_or_attribute 

		if datatypes.infertype(value_or_attribute) == 'STRING':
			value_equiv = "'" + value_or_attribute + "'"
		else:
			if attribute_type in equiv_types:
				value_equiv = equiv_types[attribute_type] + '(' + value_or_attribute + ')'
				attribute_equiv = equiv_types[attribute_type] + '(' + attribute_equiv + ')'
			else:
				value_equiv = 'str(' + value_or_attribute + ')'

		if isattribute(value_or_attribute):
			value_equiv = attribute_equiv_template % \
				(iterator, self._attribute_equiv(value_or_attribute))

		return attribute_equiv, value_equiv

	def _prefix2infix(self, expression):
	    infix = ''
	    operand = expression[0]

	    equivalent = {'=' : '==', '<>' : '!='}

	    if operand in ['and', 'or']:
	        infix += '('
	        for itm in expression[1:-1]:
	            infix += self._prefix2infix(itm)
	            infix += ' ' + operand + ' '
	        infix += self._prefix2infix(expression[-1])
	        infix += ')'

	    if operand in ['=', '<=', '>=', '<>', '<', '>']:
	        attribute, value_or_attribute = \
	        	self._attribute_value_equiv(expression[1], expression[2])

	        infix += '(%s %s %s)' % \
	            (attribute, equivalent[operand] if operand in equivalent else operand, \
	                value_or_attribute)

	    if operand == 'not':
	        attribute = expression[1]
	        infix += '(not %s)' % attribute

	    return infix

	def select(self, condition):

		parsed_condition = self._prefix2infix(condition)[1:-1]

		resulting_name = self.name + '_selection_' + self._random_string()
		resulting_type = self.types
		resulting_relation = Relation(resulting_name, resulting_type, self.attributes)
		
		for tpl in self.tuples:
			if eval(parsed_condition):
				resulting_relation.insert(self.tuples[tpl].data)

		return resulting_relation

	def type_compatible(self, that):
		return self.types == that.types

	def normalize_attributes(self, that):

		resulting_attributes = [_ for _ in self.attributes]

		for attribute in that.attributes:
			if attribute in self.attributes:
				resulting_attributes.append(that.name + '.' + attribute)
			else:
				resulting_attributes.append(attribute)

		return resulting_attributes

	def union(self, that):
		if not self.type_compatible(that):
			_callerror(self._ERROR05 % \
				('union', self.name, that.name))
			return

		resulting_name = self.name + '_union_' + \
			that.name + '_' + self._random_string()
		resulting_type = self.types
		resulting_tuples = dict(list(self.tuples.items()) + list(that.tuples.items()))
		resulting_relation = Relation(resulting_name, resulting_type, self.attributes)

		for tpl in resulting_tuples: 
			resulting_relation.insert(resulting_tuples[tpl].data)

		return resulting_relation

	def intersection(self, that):
		if not self.type_compatible(that):
			_callerror(self._ERROR05 % \
				('inter', self.name, that.name))
			return

		resulting_name = self.name + '_inter_' + \
			that.name + '_' + self._random_string()
		resulting_type = self.types
		resulting_tuples = {x : self.tuples[x] for x in self.tuples if x in that.tuples}
		resulting_relation = Relation(resulting_name, resulting_type, self.attributes)

		for tpl in resulting_tuples: 
			resulting_relation.insert(resulting_tuples[tpl].data)

		return resulting_relation

	def difference(self, that):
		if not self.type_compatible(that):
			_callerror(self._ERROR05 % \
				('diff', self.name, that.name))
			return

		resulting_name = self.name + '_diff_' + \
			that.name + '_' + self._random_string()
		resulting_type = self.types
		resulting_tuples = {x : self.tuples[x] for x in self.tuples if x not in that.tuples}
		resulting_relation = Relation(resulting_name, resulting_type, self.attributes)

		for tpl in resulting_tuples: 
			resulting_relation.insert(resulting_tuples[tpl].data)

		return resulting_relation

	def cross(self, that):

		resulting_name = self.name + '_cross_' + \
			that.name + '_' + self._random_string()
		resulting_type = self.types + that.types
		resulting_attributes = self.normalize_attributes(that)

		resulting_relation = Relation(resulting_name, resulting_type, resulting_attributes)

		for self_tpl in self.tuples:
			for that_tpl in that.tuples:
				resulting_relation.insert(self.tuples[self_tpl].data + \
					that.tuples[that_tpl].data)

		return resulting_relation

	def display(self):
		table = []

		for tpl in self.tuples:			
			table.append(self.tuples[tpl])

		print tabulate.tabulate(table, self.attributes, tablefmt="grid")

	def save(self):
		ans = 'RELATION %s {\n' % self.name

		for i, attribute in enumerate(self.attributes):
			ans += '\t%s : %s\n' % (attribute, self.types[i])

		ans += '}\n\n'		

		for tpl in self.tuples:
			aux = 'INSERT ('
			value = self.tuples[tpl].data

			for itm in value: aux += itm + ', '

			aux = aux[:-2] + ') INTO %s\n' % self.name
			ans += aux

		return ans

	def _random_string(self):
		n = 6
		seed = string.ascii_uppercase + string.digits
		return ''.join(random.choice(seed) for _ in range(n))

	def tolatex(self, caption=''):
		latex, header = '\\begin{table}[h!]\n\centering\n', ''

		for itm in self.attributes:  header += itm + ' & '

		header = header[:-3]
		latex += '\\begin{tabular}{||%s||}\n' % (self.arity * 'c ')[:-1]
		latex += '\t\hline\n'
		latex += '\t%s \\\\ [0.5ex]\n' % header
		latex += '\t\hline\hline\n'

		for _hash in self.tuples:
			_tuple = '\t\t'
			_tuple += ' & '.join(self.tuples[_hash].data)
			_tuple += ' \\\\\n'
			latex += _tuple

		latex = latex[:-1]	
		latex += ' [1ex]\n'
		latex += '\t\hline\n\end{tabular}\n'
		latex += ('\caption{%s}\n' % caption) if caption else ''
		latex += '\label{table:relation_%s}\n' % self.name.lower()
		latex += '\end{table}\n'

		return latex

	def tohtml(self):
		pass

	def toxml(self):
		pass

	def tojson(self):
		pass

	def tocsv(self):
		pass


r1 = Relation('employee', ['STRING', 'STRING', 'INTEGER'], ['name', 'lastname', 'salary'])
r2 = Relation('person', ['STRING', 'STRING', 'INTEGER'], ['name', 'lastname', 'age'])

r1.insert(('"Alonso"', '"Perez"', '100'))
r1.insert(('"Rodolfo"', '"Benitez"', '50'))
r2.insert(('"Elizabeth"', '"Baranza"', '45'))
r2.insert(('"Rodolfo"', '"Benitez"', '50'))

t1 = Tuple(("Roberto", "Almagro"))
t2 = Tuple(("Almagro", "Roberto"))
t3 = Tuple(("Almagro", "Roberto"))

'''


print t1.hash
print t2.hash
print t3.hash
# r.display()
# r.delete(('"Rodolfo"', '"Benitez"', '50'))
r1.display()
r2.display()

r3 = r1.union(r2)

r3.display()

r4 = r1.intersection(r2)
r4.display()

r5 = r2.difference(r1)
r5.display()

'''
graduates = Relation('graduates', ['INTEGER', 'STRING', 'INTEGER'], ['number', 'surname', 'age'])
graduates.insert(('7274', '"Robinson"', '37'))
graduates.insert(('7432', '"O\'Malley"', '39'))
graduates.insert(('9824', '"Darkes"', '38'))

managers = Relation('managers', ['INTEGER', 'STRING', 'INTEGER'], ['number', 'surname', 'age'])
managers.insert(('9297', '"O\'Malley"', '56'))
managers.insert(('7432', '"O\'Malley"', '39'))
managers.insert(('9824', '"Darkes"', '38'))

'''
union = graduates.union(managers)
union.display()

inter = graduates.intersection(managers)
inter.display()

diff = graduates.difference(managers)
diff.display()
'''