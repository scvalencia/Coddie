import sys
import relation
import dmlparser
import datatypes

URL = 'https://github.com/scvalencia/Burp'

VERSION = '0.1.1'

RELEASE_DATE = '2016-04-17'

WELCOME_MESSAGE = ('\n\n-----------	|	BURP - An Interpreter for Extended Relational Algebra\n'
						'\         /	|	\n'
						' \       /	|	Documentation %s\n'
						'  =======       |	Type "(help)" for help.\n'
						' /       \	|	\n'
						'/         \	|	\n'
						'-----------	|	Version %s (%s)\n') % (URL, VERSION, RELEASE_DATE)

EXIT_MESSAGE = '[Process completed]'

PROMPT = '>>> '

''' The envirment, which is supposed to be loaded from the file '''
env = {}

def _print(str):
	''' Prints the given string using low level features provided
		by the Python's standard library.
	'''

	#################################################################################
	# _print
	#################################################################################

	sys.stdout.flush()
	sys.stdout.write(str)

	#################################################################################
	# _print
	#################################################################################

def _println(str):
	''' Prints the given string, being supported by _print, adding
		a new line at the end of the message.
	'''

	#################################################################################
	# _println
	#################################################################################

	_print(str + '\n')

	#################################################################################
	# _println
	#################################################################################

def _eval_io_instruction(x):
	''' Evaluates some expression in the IO category of evaluation,
		that is, expressions that interacts with the world, that means 
		to save the enviroment or part of it to a file, to retrieve 
		relations from a file, to display a relation, or to show the 
		current state of the enviroment.
	'''

	#################################################################################
	# _eval_io_instruction
	#################################################################################

	global env

	ERROR01 = 'Error while parsing save statement, missing arguments'
	ERROR02 = 'The given string doesn\'t represent a relation: %s'
	ERROR03 = 'Error while saving relation(s) inf the given file: %s'
	ERROR04 = 'Error while parsing export statement, undefined option'
	ERROR05 = 'The given expression, does not evaluates to a relation'
	ERROR06 = '%s, is not an allowed option'

	command = x[0]

	# Save one, or several relations into a '.burp' file
	if command == 'save':
		
		if len(x) != 3:
			_println(ERROR01)
		else:
			tosave, filename, ans = x[1], x[2].replace('"', ''), ''			
			# Saving several relations
			if isinstance(tosave, list):
				for relation in tosave:
					relation = _eval(relation)

					if relation == None:				# Unsuccessful evaluation
						_println(ERROR05); return
					if relation not in env:				# Not a relation
						_println(ERROR02 % relation); return

					relation = env[relation]
					ans += relation.save()
			else:
				# Saving every relation in the enviroment
				if tosave == '*':
					for relation in env:
						relation = env[relation]
						ans += relation.save() + '\n'
				# Saving a single relation
				else:
					relation = _eval(tosave)

					if relation == None:				# Unsuccessful evaluation
						_println(ERROR05); return

					if relation not in env:				# Not a relation
						_println(ERROR02 % relation); return

					relation = env[relation]
					ans += relation.save()

			try:
				fileobject = open(filename, 'w')
				fileobject.write(ans[:-1])
			except Exception as e:
				_println(ERROR03); _println(e); return

	# TODO, comment it, and check syntax and semantics
	elif command == 'fetch':							# Unsuccessful file I/O
		filename = x[1].replace('"', '')

		try:
			env = dmlparser.parsefile(filename)
		except:
			_println('Error while loading file \'%s\'' % filename)
			_print('')

	# TODO, comment it, and check syntax and semantics
	elif command == 'display':
		relation = _eval(x[1])
		print
		env[relation].display()
		print

		# Garbage collection of intermediate relation
		if relation != x[1]:
			relation = env[relation]
			env.pop(relation.name)

	elif command == 'export':

		if len(x) < 3:
			_println(ERROR03)
		else:
			relation = _eval(x[1])
			option = x[2]

			if relation == None:				# Unsuccessfule evaluation
				_println(ERROR05)
				return

			# LaTeX branch
			if option == '"latex"' or option == "'latex'":
				# Optional caption
				caption = x[3][1:-1] if len(x) == 4 else ''
				relation = env[relation]
				latex_string = relation.tolatex(caption)
				print
				_println(latex_string)

			# Another branch
			else:
				_println(ERROR06 % option)


	# TODO, comment it, and check syntax and semantics
	elif command == 'env':
		sys.stdout.flush()
		for relation in env:
			envmessage = relation + ' : ' + str(tuple(env[relation].types))
			_println(envmessage)

	#################################################################################
	# _eval_io_instruction
	#################################################################################

def _eval_model_instruction(query):
	''' Evaluates some expression in the MODEL category of evaluation,
		that is, expressions that manipulate a single relation by 
		modeling it, or altering it by deleting tuples on it, 
		or inserting tuples on it, also to assign relations to names, 
		or rename attributes from a relation, etc.
	'''

	def _handle_name(name, string_type):
		''' Checks whether or not, a given string match the specification
			for an attribute name, or a relation name. A relation name, must
			contain letters, while an attribute name, must contain, jusr lowercase
			letters
		'''

		#################################################################################
		# _handle_name
		#################################################################################

		global env

		ERROR01 = 'Wrong %s name %s while creating relation'

		# It is a relation, or an attribute?
		condition = (lambda ch : not ch.isalpha()) if string_type == \
				'relation' else (lambda ch : not ch.isalpha() or not ch.islower())

		# Hor each character, check the condition
		for ch in name:
			if condition(ch): 
				_println(ERROR01 % (string_type, name))
				return False

		return True

		#################################################################################
		# _handle_name
		#################################################################################

	def _create():
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

		#################################################################################
		# _create
		#################################################################################

		global env

		ERROR01 = 'Error while parsing create statement, malformed statement'
		ERROR02 = ('Error while creating relation %s. Arity of types, must be the same as '
					'arity of attributes')
		ERROR03 = 'Error while creating relation %s : %s is not a valid type'
		ERROR04 = 'Error while creating relation %s : arity must be bigger than zero'

		if len(query) != 4:
			_println(ERROR01)								# Malformed create command
			return

		# The arguments, the name of the new relation, its types and attributes
		relname, types, attributes = query[1], query[2], set(query[3])

		if not _handle_name(relname, 'relation'):			# Wrong identifier for relation's name
			return

		if len(types) == 0 or len(attributes) == 0:			# Empty schema or empty types
			_println(str(ERROR04 % relname))
			return 

		if len(types) != len(attributes):					# Arity mismatch
			_println(str(ERROR02 % relname))
			return

		for t in types:										# Check for each type
			if t not in dmlparser.TYPES:
				_println(ERROR03 % (relname, t))
				return

		for a in attributes:								# Check for each attribute
			if not _handle_name(a, 'attribute'):
				return

		# Finally, insert the relation in the enviroment, and return its name
		env[relname] = relation.Relation(relname, types, list(attributes))
		return relname

		#################################################################################
		# _create
		#################################################################################

	def _insert():
		''' Insert a tuple in a relation, the syntax and semantics, is
			specified as follows:

			(insert rel (val1 ... valn))
				where rel, is the name of a relation, or an expression
				that evaluates to a relation the name of a relation, evaluates
				to a relation.

				val1 ... val, is a list of n values which forms a tuple to insert
				in the relation that evaluates to rel
		'''

		#################################################################################
		# _insert
		#################################################################################

		global env

		ERROR01 = 'Error while parsing insert statement, malformed statement'
		ERROR02 = 'Error while inserting tuple in relation, unbound relation %s'
		ERROR03 = ('Error while inserting tuple into the %s relation. '
			'Relation\'s arity is %d, but receive a %d-tuple')
		ERROR04 = ('Error while inserting tuple into the %s relation'
			'\n\tRelation\'s type is: %s.\n\tTuple\'s type is: %s')
		ERROR05 = ('The given expression, does not evaluates to a relation')

		if len(query) != 3:						
			_println(ERROR01)								# Malformed insert command
			return

		# The arguments, the evaluation of relation, and the tuple to insert
		relation, values = _eval(query[1]), query[2]

		if relation == None:								# Unsuccessfule evaluation
			_println(ERROR05)
			return

		if relation not in env:								# There's not such relation in env
			_println(ERROR02 % relation)
			return		

		relation = env[relation]							# The relation object
		if len(values) != relation.arity:					# Arity mismatch leads to an error
			_println(ERROR03 % \
			 		(relation.name, relation.arity, len(values)))
			return

		reltype = [t for _, t in relation.schema]			# The type of the relation
		tpltype = [datatypes.infertype(i) for i in values]	# The type of the given tuple

		if reltype != tpltype:								# Type mismatch leads to an error
			_println(ERROR04 %\
					(relation.name, tuple(reltype), tuple(tpltype)))
			return

		relation.insert(values)								# Finally, if this point is reached
															# insert the tuple, via the kernel

		#################################################################################
		# _insert
		#################################################################################

	#################################################################################
	# _eval_model_instruction
	#################################################################################

	command = query[0]				# The command, that determines the evaluation

	if command == 'create':			# Create a relation
		return _create()

	elif command == 'insert': 		# Insert a tuple in a relation
		return _insert()

	#################################################################################
	# _eval_model_instruction
	#################################################################################

def _eval_algebra_instruction(query):
	''' Evaluates some expression in the ALGEBRA category of evaluation,
		that is, expressions related to the Codd's definition of relational
		algebra operations, such as select, project, etc. 
	'''

	def _project():

		ERROR01 = 'Error while parsing project statement, malformed statement'
		ERROR02 = 'The given expression, does not evaluates to a relation'
		ERROR03 = 'Error while projecting the relation, unbound relation %s'
		ERROR04 = ('Error while projecting the relation, unbound attribute %s' 
						'in the relation %s')

		if len(query) != 3:			# Malformed project command
			_println(ERROR01)
			return

		# The arguments, the evaluation of relation, and the attributes to project
		relation, pattributes = _eval(query[1]), query[2]

		if relation == None:		# Unsuccessfule evaluation
			_println(ERROR02)
			return 

		if relation not in env:		# There's not such relation in env							# There's not such relation in env
			_println(ERROR03 % relation)
			return	

		relation = env[relation]
		for patt in pattributes:
			if patt not in [a for a, _ in relation.schema]:
				_println(ERROR04 % (patt, relation.name))
				return
				
		projrel = relation.project(pattributes)
		projrelname = projrel.name
		env[projrelname] = projrel
		return projrelname

	#################################################################################
	# _eval_algebra_instruction
	#################################################################################

	command = query[0]

	if command == 'project':
		return _project()

	#################################################################################
	# _eval_algebra_instruction
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

	#################################################################################
	# _eval
	#################################################################################

	global env

	ERROR01 = 'Unbound exit call'

	# Instructions classification
	instructions = {

					'IO' : 
						['save', 'fetch', 'display', 'env', 'exec', 'export'],

					'MODEL' : 
						['create', 'insert'],

					'ALGEBRA' :
						['project'],

					}

	if query == []:
		return None

	command = query[0]							# The command, that determines the evaluation
	
	if command in instructions['IO']: 			# IO operations
		_eval_io_instruction(query)

	elif command in instructions['MODEL']: 		# MODEL operations
		return _eval_model_instruction(query)

	elif command in instructions['ALGEBRA']:	# Pure relational algebra operations
		return _eval_algebra_instruction(query)

	elif type(query) == str:					# A symbol, or an atom
		return query

	elif command == 'exit':						# Exit from the Burp system

		if len(query) != 1:						# Malformed exit command
			_println(ERROR01)
			return

		_println('\n' + EXIT_MESSAGE )
		exit()

	#################################################################################
	# _eval
	#################################################################################

def _read():
	''' Read the query, and return an internal representation of it.
		Dynamically forms the query, which is given as an s-expression.
		The input process finishes when the input is balanced. Once that
		happens, the query must be parsed, and that internal representation
		is the return value
	'''

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

		#################################################################################
		# __normalize
		#################################################################################

		ERROR01 = 'EOL reached while scanning string literal'

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
						except: _println(ERROR01); break

						if next_token[-1] != '"':
							current += next_token + ' '
						else:
							current += next_token
							flag = False

						j = j + 1

					actualtokens.append(current)
					i = j

				else:
					# A string without spaces, 
					# or an atom, or an identifier, or a symbol
					actualtokens.append(token)
					i += 1

		return actualtokens

		#################################################################################
		# __normalize
		#################################################################################

	def __parse(tokens):
		''' Return an internal representation equivalent to that
			given by the s-expression parsed in the parameters,
			every internal s-expression is represented by a list,
			an atom, is represented by itself, and that is applied
			recursively. It avoids handling string separated with
			'"', that's the job of __normalize()
		'''

		#################################################################################
		# __parse
		#################################################################################

		ERROR01 = 'Unexpected EOF while reading query'
		ERROR02 = 'Unexpected \')\' while reading query'

		# Empty s-expression
		if len(tokens) == 0:
			_println(ERROR01); return

		# First item, it is an atom, or an s-expression
		token = tokens.pop(0)
		if '(' == token:						# Opens an s-expression
			ast = []							# Internal representation of tokens
			while tokens[0] != ')': 			# Porcess until ')' is found
				ast.append(__parse(tokens))		# Append inner expression
			tokens.pop(0)						# Get rid of ')'
			return ast
		elif ')' == token:						# That is a malformed s-expression
			_println(ERROR02); return
		else:
			return str(token)					# That's an atom

		#################################################################################
		# __parse
		#################################################################################

	#################################################################################
	# _read()
	#################################################################################

	ERROR01 = 'Error while parsing query'

	query, ch, level = '', '', 0	# Input handling and processing
	balanced, balance = False, 0	# Balance checking

	_print(PROMPT)

	''' While the s-expression is not balanced, process the input
		character per character. If the character is a new line, it
		treats it like an space, and increase by one the value of the 
		level. The balanced variable, depends on the number of '(',
		and ')'
	'''

	while not balanced:
		ch = sys.stdin.read(1)
		if ch != '\n':
			if ch == '(': 
				balance += 1
			elif ch == ')':
				balance -= 1

			if balance < 0: 
				_print(ERROR01)
				break

			balanced, query = balance == 0, query + ch		
			if balanced: break

		else:
			# Empy string
			if query.strip() == '': return []

			level, query = level + 1, query + ' '
			_print('\t' * level)

	sys.stdin.read(1)		# Weird, that should be added to avoid space in the next prompt

	# Pre-processing requiered for the parsing
	query = query.strip()
	if query == '': return []
	tokens = query.replace('(', ' ( ').replace(')', ' ) ').split()

	# Parsing and sting handling via __parse and __normalize respectively
	tokens = __parse(tokens)
	tokens = __normalize(tokens)

	return tokens

	#################################################################################
	# _read()
	#################################################################################

def REPL():
	''' Read queries from the command line, processes them, first
		converting them to an internal representation, then evaluates
		the query, and print the result of it (if needded)
	'''

	#################################################################################
	# REPL()
	#################################################################################

	print WELCOME_MESSAGE 

	# READ, EVALUATE, AND PRINT LOOP
	while True:
		ast = _read()
		if len(ast) != 0:
			# DEBUGGING: _println(str(ast))
			_eval(ast)
			pass
		_print('')

	#################################################################################
	# REPL()
	#################################################################################

if __name__ == '__main__':
	REPL()