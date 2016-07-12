import re
import datatypes
import relation

ERROR01 = 'Not a Coddie DML file'

ERROR02 = 'Error while parsing relation declaration at line %d'

ERROR03 = 'Wrong %s name %s at line %d'

ERROR04 = 'Reached EOF while parsing relation declaration'

ERROR05 = 'Error while parsing schema of relation %s at line %d'

ERROR06 = 'Repeated declaration of attribute %s at line %d'

ERROR07 = 'Malfored %s instruction at line %d'

ERROR08 = 'Unrecognized relation %s at line %d during INSERT execution'

ERROR09 = 'Error while inserting tuple into the %s relation at line %d. Relation\'s arity \
is %d, but receive a %d-tuple'

ERROR10 = 'Error while inserting tuple into the %s relation at line %d.\n\tRelation\'s type \
is: %s.\n\tTuple\'s type is: %s'

ERROR11 = 'Error while inserting tuple into the %s relation at line %d. Expecting ( but INTO found'

TYPES = ['INTEGER', 'CHAR', 'STRING', 'REAL', 'BOOL']
relations = {}

def _callerror(error):
	print error.replace('  ', ' ')

def _preamble(filename):
	try:
		filename, extension = filename.split('.')
	except: 
		_callerror(ERROR01)
		return

	if extension.lower() != 'codd': _preamble(filename)

	return filename, extension

def _handle_name(name, currentline, string_type):
	condition = (lambda ch : not ch.isalnum()) if string_type == \
			'relation' else (lambda ch : not ch.isalpha() or not ch.islower())

	for ch in name:
		if condition(ch): 
			_callerror(ERROR03 % (string_type, name, currentline))
			return

def _handle_schema(fileobject, relation_name, currentline):

	attributes = []
	_types = []

	while True:
		line = fileobject.readline()
		if not line: 
			_callerror(ERROR04)
			return

		line = line.strip()
		currentline += 1
		if not line: continue

		parse = line.split()
		if parse[0] == '}': break

		if len(parse) != 3 or parse[1] != ':' or parse[2] not in TYPES:
			_callerror(ERROR05 % (relation_name, currentline))
			return

		name, reltype = parse[0], parse[2]
		_handle_name(name, currentline, 'attribute')
		if name in attributes: 
			_callerror(ERROR06 % (name, currentline))
			return

		attributes.append(name)
		_types.append(reltype)

	return attributes, _types, currentline

def _handle_declaration(fileobject, parse, currentline):
	if len(parse) != 3 or parse[-1] != '{':
		_callerror(ERROR02 % ('INSERT', currentline))
		return

	_handle_name(parse[1], currentline, 'relation')

	relname = parse[1]

	attributes, types, currentline = _handle_schema(fileobject, relname, currentline)

	return relname, attributes, types, currentline

def _handle_insert_values(values_string):
	parse = map(lambda x : x.strip(), values_string.split(','))
	datum = []

	SEPARATOR = '"'
	current = ''

	i = 0
	while i < len(parse):
		lexeme = parse[i]
		if lexeme[0] == SEPARATOR and lexeme[-1] == SEPARATOR:
			datum.append(lexeme)
		elif lexeme[0] == SEPARATOR and lexeme[-1] != SEPARATOR:
			current += lexeme + ', '
		elif lexeme[0] != SEPARATOR and lexeme[-1] == SEPARATOR:
			current += lexeme
			datum.append(current)
			current = ''
		else:
			tpe = datatypes.infertype(lexeme)
			if tpe == 'STRING':
				current += lexeme + ', '
			else:
				datum.append(lexeme)
				current = ''
		i += 1
		
	return datum

def _handle_insertion(instruction, currentline):
	parse = instruction.split()
	name = parse[-1]
	into = parse[-2]
	if into != 'INTO': 
		_callerror(ERROR07 % ('INSERT', currentline))
		return
	if name not in relations: 
		_callerror(ERROR08 % (name, currentline))
		return

	relation = relations[name]
	m = re.search("INSERT (.*) INTO", instruction)

	if not m:
		_callerror(ERROR11 % (name, currentline))
		return

	if len(m.group(1)) == 2:		
		_callerror(ERROR11 % (name, currentline))
		return

	values_string = m.group(1)[1:-1]
	values = _handle_insert_values(values_string)

	if len(values) != relation.arity:
		_callerror(ERROR09 % (name, currentline, relation.arity, len(values)))
		return

	reltype = [t for _, t in relation.schema]
	tpltype = [datatypes.infertype(i) for i in values]

	if reltype != tpltype:
		_callerror(ERROR10 % (name, currentline, tuple(reltype), tuple(tpltype)))
		return

	return tuple(values)

def parsefile(filename):

	filename, extension = _preamble(filename)

	fileobject = open(filename + '.' + extension, 'r')
	currentline = 0

	while True:
		line = fileobject.readline()
		if not line: break

		line = line.strip()
		currentline += 1
		if not line: continue

		parse = line.split()
		if parse[0] == '--': continue

		elif parse[0] == 'RELATION':
			relname, attributes, types, currentline = \
				_handle_declaration(fileobject, parse, currentline)
			relations[relname] = relation.Relation(relname, types, attributes)

		elif parse[0] == 'INSERT':
			values = _handle_insertion(line, currentline)
			if values == None:
				break
			relations[relname].insert(values)

		else:
			_callerror(ERROR07 % ('', currentline))
			return

	return relations