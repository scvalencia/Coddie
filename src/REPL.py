import sys
import dmlparser

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

ERROR01 = 'EOL reached while scanning string literal'

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

def _eval_ioinstruction(x):
	global env

	if x[0] == 'save':
		pass
	elif x[0] == 'fetch':
		filename = x[1].replace('\'', '')
		try:
			_println(filename)
			env = dmlparser.parsefile(filename)
		except:
			_println('Error while loading file \'%s\'' % filename)
			_print('')
			env = {}
	elif x[0] == 'display':
		relation = x[1]
		print
		env[relation].display()
		print
	elif x[0] == 'env':
		sys.stdout.flush()
		for relation in env:
			envmessage = relation + ' : ' + str(tuple(env[relation].types))
			_println(envmessage)
			sys.stdout.write(envmessage + '\n')

def _eval(x):
	global env

	instructions = {'IO' : ['save', 'fetch', 'display', 'env']}

	if x[0] in instructions['IO']:
		_eval_ioinstruction(x)
	elif x[0] == 'exit':
		_println('\n' + EXIT_MESSAGE )
		exit()

def main():

	print WELCOME_MESSAGE 

	while True:
		ast = _read()
		if len(ast) != 0:
			_println(str(ast))
			_eval(ast)
		_print('')

if __name__ == '__main__':
	main()