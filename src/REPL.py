import sys
import info
import errors
import relation
import dmlparser
import datatypes

''' The envirment, which is supposed to be loaded from the file '''
env = {}

#################################################################################
# AUXILIAR FUNCTIONS
#################################################################################

def _print(str):
	''' Prints the given string using low level features provided
		by the Python's standard library.
	'''

	sys.stdout.flush()
	sys.stdout.write(str)

def _println(str):
	''' Prints the given string, being supported by _print, adding
		a new line at the end of the message.
	'''

	_print(str + '\n')

def _check_relation(relation):
	global env

	if relation == None:
		_println(errors.ERROR_EXPRESION_EVAL)
		return False

	if relation not in env:
		_println(errors.ERROR0_UNBOUND_VAR % relation)
		return False

	return True

def _check_query_length(fncmp, query, instruction, expected):
	if fncmp(len(query), expected):
		_println(errors.ERROR_MISSING_ARGS % \
			(instruction, instruction, expected, len(query)))
		return False

	return True

def _check_attribute_value_type(relation, attribute, value):
	attribute_type = relation.types[relation.attributes.index(attribute)]

	if attribute_type != datatypes.infertype(value):
		_println(errors.ERROR_SELECT_CLAUSE_TYPE1 % (attribute, value))
		return False

	return True

def _check_condition(relation, condition):
	isattribute = lambda x : x in relation.attributes

	def _check_atom(condition):

		operand, errs = condition[0], 0

		if operand in ['and', 'or']:
			for clause in condition[1:]: _check_atom(clause)

		elif operand in ['=', '<=', '>=', '<>', '<', '>']:
			# TODO: Chaek length

			attribute, value_or_attribute = condition[1], condition[2]

			if not isattribute(attribute):
				_println(errors.ERROR_SELECT_ATTRIBUTE % (attribute, relation.name))
				errs += 1

			if not isattribute(value_or_attribute) and \
				datatypes.infertype(value_or_attribute) == 'NULL':
				_println(errors.ERROR_SELECT_VALUE % (attribute, relation.name))
				errs += 1

			if not _check_attribute_value_type(relation, attribute, value_or_attribute):
				errs += 1

		elif operand == 'not':
			# TODO: Chaek length

			attribute, attribute_type = condition[1], relation.types[relation.attributes.index(attribute)]

			if not isattribute(attribute):
				_println(errors.ERROR_SELECT_ATTRIBUTE % (attribute, relation.name))
				errs += 1

			if attribute_type != 'BOOL':
				_println(errors.ERROR_SELECT_CLAUSE_TYPE2 % attribute)
				errs += 1

		else:
			_println(errors.ERROR_MALFORMED_CONDITION % operand)
			errs += 1

		return errs

	return _check_atom(condition) == 0

def _handle_name(name, string_type):
	''' Checks whether or not, a given string match the specification
		for an attribute name, or a relation name. A relation name, must
		contain letters, while an attribute name, must contain, jusr lowercase
		letters
	'''

	# It is a relation, or an attribute?
	condition = (lambda ch : not ch.isalpha()) if string_type == \
			'relation' else (lambda ch : not ch.isalpha() or not ch.islower())

	# Hor each character, check the condition
	for ch in name:
		if condition(ch): 
			_println('Wrong %s name %s while creating relation' \
				% (string_type, name)); return False
	
	return True

def _gc(relation, expression):
	global env

	if relation.name != expression: 
		env.pop(relation.name)

#################################################################################
# EVALUATION OF I/O RELATED QUERIES
#################################################################################

def _save(query):
	global env

	if not _check_query_length(lambda a, b : a != b, query, 'save', 3): 
		return

	tosave, filename, ans = query[1], query[2].replace('"', ''), ''

	if isinstance(tosave, list):
		for relation in tosave:
			relation = _eval(relation)
			if not _check_relation(relation): return
			relation = env[relation]
			ans += relation.save()

	else:
		if tosave == '*':
			for relation in env:
				relation = env[relation]
				ans += relation.save() + '\n'

		else:
			relation = _eval(tosave)
			if not _check_relation(relation): return
			relation = env[relation]
			ans += relation.save()

	try:
		fileobject = open(filename, 'w')
		fileobject.write(ans[:-1])
	except Exception as e:
		_println(ERRORS.ERROR_SAVE_FILE % filename)
		_println(str(e))
		return

def _fetch(query):
	global env

	if not _check_query_length(lambda a, b : a != b, query, 'fetch', 2): 
		return

	filename = query[1].replace('"', '')		

	try:
		dummyenv = dmlparser.parsefile(filename)
		_println('')

		for relation in dummyenv: 
			env[relation] = dummyenv[relation]
			_println("Loaded relation: " + env[relation].name)

		_println('')
	except Exception as e:
		_println(errors.ERROR_FETCH_FILE % filename)
		_println(str(e))
		return

def _execute():
	pass
	# COPY FROM READ()

def _display(query):
	global env

	if not _check_query_length(lambda a, b : a != b, query, 'display', 2): 
		return

	relation = _eval(query[1])
	if not _check_relation(relation): return
	relation = env[relation]

	print
	relation.display()
	print

	_gc(relation, query[1])

def _export(query):
	global env

	if not _check_query_length(lambda a, b : a < b, query, 'export', 3): 
		return

	relation = _eval(query[1])
	if not _check_relation(relation): return
	option = query[2]
	relation = env[relation]

	if option == '"latex"':
		caption = query[3][1:-1] if len(query) == 4 else ''
		print; _println( relation.tolatex(caption))

	else:
		_println(errors.ERROR_IMPORT_OPT % \
			(relation.name, option))
		return

	_gc(relation, query[1])

def _env(query):
	global env

	if not _check_query_length(lambda a, b : a != b, query, 'env', 1):
		return

	sys.stdout.flush()
	_println('')

	for relation in env:
		relation = env[relation]

		schema = [_attribute + ':' + _type.lower() \
				for _attribute, _type in relation.schema]

		envmessage = relation.name + '(' + ', '.join(schema) + ')'
		_println(envmessage)

	_println('')

def _eval_io_instruction(query):
	''' Evaluates some expression in the IO category of evaluation,
		that is, expressions that interacts with the world, that means 
		to save the enviroment or part of it to a file, to retrieve 
		relations from a file, to display a relation, or to show the 
		current state of the enviroment.
	'''

	function_dct = {
						'save' : _save,
						'fetch' : _fetch,
						'display' : _display,
						'export' : _export,
						'env' : _env,
				}

	command = query[0]
	return function_dct[command](query)

#################################################################################
# EVALUATION OF DATA MODELING RELATED QUERIES
#################################################################################

def _create(query):
	''' Create a tuple, and add it to the enviroment, given the name, the
		type of it and the attributes or schema
		
		(create relname (t1 ... tn) (a1 ... am))
			where relname is a valid string representing the name of the new
			relation ([A-Z][a-z])*. n, m are integers, and ti, represents the
			type of the ith attribute in the schema (ai). For succesfull 
			application, n has to be equal to m.

			Each type could be one of:
				STRING, INTEGER, CHAR, BOOL, REAL

			A valid attribute name matches ([a-z]*)

		Adds the relation to the enviroment, and returns an expression, that
		evaluates to a relation
	'''

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'create', 4): 
		return

	# The arguments, the name of the new relation, its types and attributes
	relname, types, attributes = query[1], query[2], set(query[3])

	if not _handle_name(relname, 'relation'):			# Wrong identifier for relation's name
		return

	if len(types) == 0 or len(attributes) == 0:			# Empty schema or empty types
		_println(errors.ERROR_CREATE_ARITY_ZERO \
			% relname); return 

	if len(types) != len(attributes):					# Arity mismatch
		_println(str(errors.ERROR_CREATE_ARITY_MISMATCH \
		 % relname)); return

	attributes = query[3]

	for i, _ in enumerate(types):						# Check for each type
		t, a = types[i], attributes[i]
		if t not in dmlparser.TYPES:
			_println(errors.ERROR_CREATE_TYPE 
				% (relname, t)); return
		if not _handle_name(a, 'attribute'):			# Check for each attribute
			return

	# Finally, insert the relation in the enviroment, and return its name
	env[relname] = relation.Relation(relname, types, query[3])
	return relname

def _insert(query):
	''' Insert a tuple in a relation, the syntax and semantics, is
		specified as follows:

		(insert rel (val1 ... valn))
			where rel, is the name of a relation, or an expression
			that evaluates to a relation the name of a relation, evaluates
			to a relation.

			val1 ... val, is a list of n values which forms a tuple to insert
			in the relation that evaluates to rel
	'''

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'insert', 3): 
		return

	# The arguments, the evaluation of relation, and the tuple to insert
	relation, values = _eval(query[1]), query[2]
	if not _check_relation(relation): return
	relation = env[relation]							# The relation object

	if len(values) != relation.arity:					# Arity mismatch leads to an error
		_println(errors.ERROR_INSERT_MISMATCH % \
		 		(relation.name, relation.arity, len(values))); return

	reltype = [t for _, t in relation.schema]			# The type of the relation
	tpltype = [datatypes.infertype(i) for i in values]	# The type of the given tuple

	if reltype != tpltype:								# Type mismatch leads to an error
		_println(errors.ERROR_INSERT_TYPE % \
				(relation.name, tuple(reltype), tuple(tpltype))); return

	relation.insert(values)								# Finally, if this point is reached
														# insert the tuple, via the kernel

def _eval_model_instruction(query):
	''' Evaluates some expression in the MODEL category of evaluation,
		that is, expressions that manipulate a single relation by 
		modeling it, or altering it by deleting tuples on it, 
		or inserting tuples on it, also to assign relations to names, 
		or rename attributes from a relation, etc.
	'''

	function_dct = {
						'create' : _create,
						'insert' : _insert,
				}

	command = query[0]
	return function_dct[command](query)

#################################################################################
# EVALUATION OF RELATIONAL ALGEBRA OPERATOS
#################################################################################

def _set(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'set', 3): 
		return

	relname, relation = query[1], _eval(query[2])
	if not _check_relation(relation): return
	relation = env[relation]

	env[relname] = env.pop(relation.name)
	env[relname].name = relname

	_gc(relation, query[1])
	return relation.name

def _project(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'project', 3): 
		return

	# The arguments, the evaluation of relation, and the attributes to project
	relation, pattributes = _eval(query[1]), query[2]
	if not _check_relation(relation): return
	relation = env[relation]

	for patt in pattributes:
		if patt not in [a for a, _ in relation.schema]:
			_println(errors.ERROR_PROJECT_ATTRIBUTES \
				% (patt, relation.name)); return
				
	resulting_relation = relation.project(pattributes)
	env[resulting_relation.name] = resulting_relation

	_gc(relation, query[1])
	return resulting_relation.name

def _select(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'select', 3): 
		return

	# The arguments, the evaluation of relation, and the attributes to project
	relation, predicate = _eval(query[1]), query[2]
	if not _check_relation(relation): return
	relation = env[relation]

	if not _check_condition(relation, predicate): return
	
	resulting_relation = relation.select(predicate)
	env[resulting_relation.name] = resulting_relation

	_gc(relation, query[1])
	return resulting_relation.name

def _union(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'union', 3): 
		return

	this_relation, that_relation = _eval(query[1]), _eval(query[2])
	if not _check_relation(this_relation): return
	if not _check_relation(that_relation): return
	this_relation, that_relation = env[this_relation], env[that_relation]

	if not this_relation.type_compatible(that_relation):
		_println(errors.ERROR_TYPE_COMPATIBLE % 'union'); return

	resulting_relation  = this_relation.union(that_relation)
	env[resulting_relation.name] = resulting_relation

	_gc(this_relation, query[1])
	_gc(that_relation, query[2])
	return resulting_relation.name	

def _inter(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'inter', 3): 
		return

	this_relation, that_relation = _eval(query[1]), _eval(query[2])
	if not _check_relation(this_relation): return
	if not _check_relation(that_relation): return
	this_relation, that_relation = env[this_relation], env[that_relation]

	if not this_relation.type_compatible(that_relation):
		_println(errors.ERROR_TYPE_COMPATIBLE % 'inter'); return

	resulting_relation  = this_relation.intersection(that_relation)
	env[resulting_relation.name] = resulting_relation

	_gc(this_relation, query[1])
	_gc(that_relation, query[2])
	return resulting_relation.name	

def _diff(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'diff', 3): 
		return

	this_relation, that_relation = _eval(query[1]), _eval(query[2])
	if not _check_relation(this_relation): return
	if not _check_relation(that_relation): return
	this_relation, that_relation = env[this_relation], env[that_relation]

	if not this_relation.type_compatible(that_relation):
		_println(errors.ERROR_TYPE_COMPATIBLE % 'diff'); return

	resulting_relation  = this_relation.difference(that_relation)
	env[resulting_relation.name] = resulting_relation

	_gc(this_relation, query[1])
	_gc(that_relation, query[2])
	return resulting_relation.name

def _cross(query):

	global env

	if not _check_query_length(lambda a, b : a != b, query, 'cross', 3): 
		return

	this_relation, that_relation = _eval(query[1]), _eval(query[2])
	if not _check_relation(this_relation): return
	if not _check_relation(that_relation): return
	this_relation, that_relation = env[this_relation], env[that_relation]

	resulting_relation  = this_relation.cross(that_relation)
	env[resulting_relation.name] = resulting_relation

	_gc(this_relation, query[1])
	_gc(that_relation, query[2])
	return resulting_relation.name

def _eval_algebra_instruction(query):
	''' Evaluates some expression in the ALGEBRA category of evaluation,
		that is, expressions related to the Codd's definition of relational
		algebra operations, such as select, project, etc. 
	'''

	function_dct = {
						'project' : _project,
						'select' : _select,
						'union' : _union,
						'inter' : _inter,
						'diff' : _diff,
						'cross' : _cross,
						'set' : _set,
				}

	command = query[0]
	return function_dct[command](query)

#################################################################################
# EVALUATION MAIN PROCEDURE
#################################################################################

def _eval(query):
	''' Evaluates a query depending its kind. That is, the first 
		word of the tokens processed by _read(). The query can alter
		the state of the enviroment, the state of a relation, or retrieve
		information out of the relations using operations whose semantics
		is the same as in relational algebra (Codd's one).

		A query can be of the following kinds:

			IO : interact with the world, that is, to save the enviroment or part
			of it to a file, to retrieve relations from a file, to display a relation,
			or to show the state of the enviroment.

			MODEL: manipulate a single relation by modeling it, or altering it by
			deleting tuples on it, or inserting tuples on it, also to assign relations
			to names, or rename attributes from a relation.

		The responsability for each kind of evaluation, is delegated to other
		functions.
	'''

	global env

	# Instructions classification
	instructions = {

					'IO' : 
						['save', 'fetch', 'display', 'export', 'env'],

					'MODEL' : 
						['create', 'insert'],

					'ALGEBRA' :
						['set', 'project', 'select', 'union', 'inter', 'diff', 'cross'],

					}

	if query == []: return None

	command = query[0]							# The command, that determines the evaluation
	
	if command in instructions['IO']: 			# IO operations
		_eval_io_instruction(query)

	elif command in instructions['MODEL']: 		# MODEL operations
		return _eval_model_instruction(query)

	elif command in instructions['ALGEBRA']:	# Pure relational algebra operations
		return _eval_algebra_instruction(query)

	elif type(query) == str:					# A symbol, or an atom
		return query

	elif command == 'exit':						# Exit from the Coddie system

		if len(query) != 1:						# Malformed exit command
			_println('Unbound exit call')
			return

		_println('\n' + info.EXIT_MESSAGE )
		exit()

#################################################################################
# REPL RELATED FUNCTIONS
#################################################################################

def __normalize(tokens):
	''' Return an internal representation equivalent to that
		given by the s-expression parsed by __parse, with the,
		difference that __normalize takes into account strings
		with spaces, such as "This is an example". For example
		for the next query, the result by __parse and __normalize 
		is exposed:

		(select relation (and (= name "Edgar Codd")))

		__parse:
			['select', 'relation', ['and', ['=', 'name', '"Edgar', 'Codd"']]]
		__normalize:
			['select', 'relation', ['and', ['=', 'name', '"Edgar Codd"']]]

		So the string "Edgar code", could be treated as an atom
	'''

	i = 0
	actualtokens = []	
	# Traverse tokens and process strings and atoms								
	while i < len(tokens):
		token = tokens[i]								# Current token
		if isinstance(token, list):						# If is a list, then use recursion
			actualtokens.append(__normalize(token))
			i += 1
		else:											# Otherwise, could be an atom, a string
														# without spaces, or a string with spaces

			if token[0] == '"' and token[-1] != '"':
				# A string with spaces
				current, j, flag = token + ' ', i + 1, True
				while flag:
					try: next_token = tokens[j]
					except: _println('EOL reached while scanning string literal'); break

					if next_token[-1] != '"':
						current += next_token + ' '
					else:
						current += next_token; flag = False

					j = j + 1

				actualtokens.append(current)
				i = j
			else:
				# A string without spaces, 
				# or an atom, or an identifier, or a symbol
				actualtokens.append(token)
				i += 1

	return actualtokens

def __parse(tokens):
	''' Return an internal representation equivalent to that
		given by the s-expression parsed in the parameters,
		every internal s-expression is represented by a list,
		an atom, is represented by itself, and that is applied
		recursively. It avoids handling string separated with
		'"', that's the job of __normalize()
	'''

	# Empty s-expression
	if len(tokens) == 0:
		_println('Unexpected EOF while reading query'); return

	# First item, it is an atom, or an s-expression
	token = tokens.pop(0)
	if '(' == token:						# Opens an s-expression
		ast = []							# Internal representation of tokens
		while tokens[0] != ')': 			# Porcess until ')' is found
			ast.append(__parse(tokens))		# Append inner expression
		tokens.pop(0)						# Get rid of ')'
		return ast
	elif ')' == token:						# That is a malformed s-expression
		_println('Unexpected \')\' while reading query'); return
	else:
		return str(token)					# That's an atom

def _read():
	query, ch, level = '', '', 0	# Input handling and processing
	balanced, balance = False, 0	# Balance checking

	_print(info.PROMPT)

	# while the s-expression is not balanced, process the input
	# character per character. If the character is a new line, it
	# treats it like an space, and increase by one the value of the 
	# level. The balanced variable, depends on the number of '(',
	# and ')'

	while not balanced:
		ch = sys.stdin.read(1)
		if ch != '\n':
			if ch == '(':  balance += 1
			elif ch == ')': balance -= 1

			if balance < 0: 
				_print('Error while parsing query'); break

			balanced, query = balance == 0, query + ch	

			if balanced: break

		else:
			# Empy string
			if query.strip() == '': return []
			level, query = level + 1, query + ' '
			_print('\t' * level)

	sys.stdin.read(1)		# Weird. This should be added to avoid space in the next prompt

	# Pre-processing requiered for the parsing
	query = query.strip()
	if query == '': return []
	tokens = query.replace('(', ' ( ').replace(')', ' ) ').split()

	# Parsing and sting handling via __parse and __normalize respectively
	tokens = __parse(tokens)
	tokens = __normalize(tokens)

	return tokens

def REPL():
	''' Read queries from the command line, and processes them first
		converting them to an internal representation, then evaluates
		the query, and prints the result of it (if needded)
	'''

	print info.WELCOME_MESSAGE 

	# READ, EVALUATE, AND PRINT LOOP
	while True:
		ast = _read()
		if len(ast) != 0:
			_eval(ast)
		_print('')

if __name__ == '__main__':
	REPL()