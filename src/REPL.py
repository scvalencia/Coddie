import sys
import relation
import dmlparser
import datatypes

URL = 'https://github.com/scvalencia/Burp'
VERSION = '0.1.1'
RELEASE_DATE = '2016-04-17'

WELCOME_MESSAGE = ('\n\n-----------	|	BURP - An Extended Interpreter of the Relational Algebra\n'
						'\         /	|	\n'
						' \       /	|	Documentation %s\n'
						'  =======       |	Type "(help)" for help.\n'
						' /       \	|	\n'
						'/         \	|	\n'
						'-----------	|	Version %s (%s)\n') % (URL, VERSION, RELEASE_DATE)

EXIT_MESSAGE = '[Process completed]'

env = {}

def _print(str):
	sys.stdout.flush()
	sys.stdout.write(str)

def _println(str):
	_print(str + '\n')

def _parse(tokens):
    if len(tokens) == 0:
    	# Syntax error: unexpected EOF while reading query
    	pass

    token = tokens.pop(0)
    if '(' == token:
        ast = []
        while tokens[0] != ')':
            ast.append(_parse(tokens))
        tokens.pop(0)
        return ast
    elif ')' == token:
		# Syntax error: unexpected ')' while reading program
		pass
    else:
        return str(token)

def _normalize(tokens):
	ERROR01 = 'EOL reached while scanning string literal'
	
	i = 0
	actualtokens = []
	while i < len(tokens):
		token = tokens[i]
		if isinstance(token, list):
			actualtokens.append(_normalize(token))
			i += 1
		else:
			if token[0] == '"' and token[-1] != '"':
				current = token + ' '
				j = i + 1
				flag = True
				while flag:
					try:
						next_token = tokens[j]
					except:
						_println(ERROR01)
						break
					if next_token[-1] != '"':
						current += next_token + ' '
					else:
						current += next_token
						flag = False
					j = j + 1
				i = j + 1
				actualtokens.append(current)
			elif token[0] == token[-1] == '"':
				actualtokens.append(token)
				i += 1
			else:
				actualtokens.append(token)
				i += 1

	return actualtokens

def _read():
	query = ''
	ch = ''
	stack = []
	balanced = False
	balance = 0
	level = 0
	print '>>> ',
	while not balanced:
		ch = sys.stdin.read(1)
		if ch != '\n':
			if ch == '(': balance += 1
			elif ch == ')':
				balance -= 1
				if balance < 0: print 'error'; break
			balanced = balance == 0
			query += ch
			if balanced: break
		else:
			if query.strip() == '': return []
			level += 1
			_print('\t' * level)
			query += ' '

	sys.stdin.read(1)
	query = query.strip()
	if query == '': return []
	tokens = query.replace('(', ' ( ').replace(')', ' ) ').split()
	return _normalize(_parse(tokens))

def _eval_io_instruction(x):
	global env

	command = x[0]

	if command == 'save':
		pass
	elif command == 'fetch':
		filename = x[1].replace('\'', '')
		try:
			_println(filename)
			env = dmlparser.parsefile(filename)
		except:
			_println('Error while loading file \'%s\'' % filename)
			_print('')
			env = {}
	elif command == 'display':
		relation = x[1]
		print
		env[relation].display()
		print
	elif command == 'env':
		sys.stdout.flush()
		for relation in env:
			envmessage = relation + ' : ' + str(tuple(env[relation].types))
			_println(envmessage)

def _eval_model_instruction(query):
	global env

	ERROR01 = 'Error while parsing create statement, malformed statement'
	ERROR02 = 'Wrong %s name %s while creating relation'
	ERROR03 = ('Error while creating relation %s. Arity of types, must be the same as '
					'arity of attributes')
	ERROR04 = 'Error while creating relation: %s is not a valid type'
	ERROR05 = 'Error while parsing insert statement, malformed statement'
	ERROR06 = 'Error while inserting tuple in relation, unbound relation %s'
	ERROR07 = ('Error while inserting tuple into the %s relation.'
		'Relation\'s arity is %d, but receive a %d-tuple')
	ERROR08 = ('Error while inserting tuple into the %s relation'
		'\n\tRelation\'s type is: %s.\n\tTuple\'s type is: %s')

	def _handle_name(name, string_type):
		condition = (lambda ch : not ch.isalpha()) if string_type == \
				'relation' else (lambda ch : not ch.isalpha() or not ch.islower())

		for ch in name:
			if condition(ch): 
				_println(ERROR02 % (string_type, name))
				return False

		return True

	def _create():
		if len(query) != 4:
			_println(ERROR01)
			return

		relname, types, attributes = query[1], query[2], set(query[3])
		if not _handle_name(relname, 'relation'):
			return

		if len(types) != len(attributes):
			_println(str(ERROR03 % relname))
			return

		for t in types:
			if t not in dmlparser.TYPES:
				_println(ERROR04 % t)
				return

		env[relname] = relation.Relation(relname, types, attributes)
		return relname

	def _insert():
		if len(query) != 3:
			_println(ERROR05)
			return

		relation, values = _eval(query[1]), query[2]
		if relation not in env:
			_println(ERROR06)
			return

		relation = env[relation]
		if len(values) != relation.arity:
			_println(ERROR07 % (relation.name, relation.arity, len(values)))
			return

		reltype = [t for _, t in relation.schema]
		tpltype = [datatypes.infertype(i) for i in values]

		if reltype != tpltype:
			_println(ERROR08 % (relation.name, tuple(reltype), tuple(tpltype)))
			return

		relation.insert(values)

	command = query[0]

	if command == 'create':	return _create()
	elif command == 'insert': return _insert()


def _eval(query):
	global env

	ERROR01 = 'Unbound exit call'

	instructions = {'IO' : ['save', 'fetch', 'display', 'env'],
					'MODEL' : ['create', 'insert']}

	command = query[0]
	
	if command in instructions['IO']: _eval_io_instruction(query)
	elif command in instructions['MODEL']: return _eval_model_instruction(query)
	elif command == 'exit':
		if len(query) != 1:
			_println(ERROR01)
			return
		_println('\n' + EXIT_MESSAGE )
		exit()

def REPL():

	print WELCOME_MESSAGE 

	while True:
		ast = _read()
		if len(ast) != 0:
			# DEBUGGING: _println(str(ast))
			_eval(ast)
		_print('')

if __name__ == '__main__':
	REPL()