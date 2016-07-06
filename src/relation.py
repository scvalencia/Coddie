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

		if t.arity != self.arity:
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
		resulting = Relation(resulting_name, resulting_type, arguments)
		
		for tpl in self.tuples:
			lst = [self.tuples[tpl][idx] for idx in idxs]
			resulting.insert(tuple(lst))

		return resulting

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
			for itm in value:
				aux += itm + ', '
			aux = aux[:-2] + ') INTO %s\n' % self.name
			ans += aux

		return ans

	def _random_string(self):
		n = 6
		seed = string.ascii_uppercase + string.digits
		return ''.join(random.choice(seed) for _ in range(n))

	def tolatex(self, caption=''):
		latex, header = '\\begin{table}[h!]\n\centering\n', ''

		for itm in self.attributes: 
			header += itm + ' & '

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