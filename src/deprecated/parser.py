from pyparsing import OneOrMore, nestedExpr
import relation
import dataTypes
import pyparsing

class Env(dict):

	def __init__(self, params = (), args = (), outer = None):
		self.update(zip(params, args))
		self.outer = outer

	def find(self, var):
		return self if var in self else self.outer.find(var)


def parse_expression(expression, enviroment = Env()):
	if len(expression) == 1:
		if expression[0] in enviroment:
			relation = expression[0]
			return enviroment[relation]

	if expression[0].upper() == 'PROJECT':
		(_, parameters, exp) = expression
		parameters = [_.upper() for _ in parameters]
		if isinstance(exp, pyparsing.ParseResults):
			rel = parse_expression(exp, enviroment)
			enviroment[rel.name] = rel
			return parse_expression(exp, enviroment)
			#return rel.project(parameters, enviroment)
		else:
			if exp in enviroment:
				return enviroment[exp].project(parameters)

	elif expression[0].upper() == 'SELECT':
		(_, boolean_expression, exp) = expression
		parse_expression(exp)

	elif expression[0].upper() == 'JOIN':
		(_, relation1, relation2) = expression
		parse_expression(relation1)
		parse_expression(relation2)

	elif expression[0].upper() == 'INSERT':
		(_, insert_tuple, relation) = expression
		if relation in enviroment:
			tuple_1 = []
			zipped_list = zip(enviroment[relation].types, insert_tuple)
			tuples_7 = []
			for itm in zipped_list:
				tuples_7.append(itm[0](itm[1]))
			ans = enviroment[relation].insert(tuples_7)
			if ans:
				return enviroment[relation]

	elif expression[0].upper() == 'DELETE':
		(_, pk, relation) = expression
		if relation in enviroment:
			ans = enviroment[relation].delete(pk)
			if ans:
				return enviroment[relation]

			

#parse_expression(data[0])

attributes = ['first_name', 'last_name', 'year', 'motive']
attributes = [_.upper() for _ in attributes]
types = [dataTypes.STRING, dataTypes.STRING, dataTypes.INT, dataTypes.STRING]
rel = relation.Relation('TuringAward', types, attributes, 'first_name'.upper())

tpl = (dataTypes.STRING('Alan'), dataTypes.STRING('Perlis'), dataTypes.INT(1966), dataTypes.STRING('Compiler construction'))
rel.insert(tpl)


tpl = (dataTypes.STRING('Maurice'), dataTypes.STRING('Wilkes'), dataTypes.INT(1967), 
	dataTypes.STRING('Computer design and APIs'))
rel.insert(tpl)


tpl = (dataTypes.STRING('Richard'), dataTypes.STRING('Hamming'), dataTypes.INT(1968), 
	dataTypes.STRING('Numerical methods and error correcting codes'))
rel.insert(tpl)


tpl = (dataTypes.STRING('Marvin'), dataTypes.STRING('Minsky'), dataTypes.INT(1969), 
	dataTypes.STRING('AI research'))
rel.insert(tpl)


tpl = (dataTypes.STRING('James'), dataTypes.STRING('Wilkinson'), dataTypes.INT(1970), 
	dataTypes.STRING('NUmerical analysis in computation'))
rel.insert(tpl)


tpl = (dataTypes.STRING('John'), dataTypes.STRING('McCarthy'), dataTypes.INT(1971), 
	dataTypes.STRING('AI research and LISP'))
rel.insert(tpl)


tpl = (dataTypes.STRING('Edsger'), dataTypes.STRING('Dijkstra'), dataTypes.INT(1972), 
	dataTypes.STRING('Development of ALGOL, and the art of programming'))
rel.insert(tpl)



global_env = Env()
global_env[rel.name] = rel

def REPL(prompt = 'BURP:> '):
	sentence = ''
	while True:
		sentence = raw_input(prompt)
		value = None
		if sentence == '(EXIT)':
			break
		elif len(sentence.split()) == 1:
			value = parse_expression([sentence], global_env)
		else:
			sentence = list(OneOrMore(nestedExpr()).parseString(sentence)[0])
			value = parse_expression(sentence, global_env)
		if value is not None:
			print global_env
			print value

REPL()