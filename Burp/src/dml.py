import sys
import os

from relation import Relation
from dataTypes import BOOL
from dataTypes import INT
from dataTypes import REAL
from dataTypes import STRING
from dataTypes import CHAR
from dataTypes import DATE


runtime = {}
rt_env = {}

def parse_file(filename):
	parse = filename.upper().split('.')
	if parse[1] == 'BURP':
		file_object = open(filename, 'r')
		representation = file_object.readlines()
		return [_ for _ in enumerate(representation)]
	else:
		print filename + ' is not a BUPR file'
		sys.exit()

def set_env(parse):

	env = {}

	name = ''
	done = False
	i = 0
	while not done:

		itm = parse[i]
		line = itm[0]
		command = itm[1]

		if 'RELATION' in command:
			name = parse[i][1].split()[1]
			j = i
			while not '{' in parse[j][1]:
				if i == j: j += 1
				if parse[j][1].strip():
					print 'Error while parsing file, expected \'{\', found ' + parse[j][1]
					print 'Line: ' + str(j + 1)
					sys.exit()
				j += 1

			if i == j: 
				i = j + 1
			else:
				i = j

			variables = ''

			while not '}' in parse[i][1]:
				variables += parse[i][1].strip()
				if 'INSERT' in parse[i][1]:
					print 'Error while parsing the file, expected \'}\', found ' + parse[i][1]
					print 'Line: ' + str(i + 1)
					sys.exit()
				i += 1

			variables = variables.replace('{', '')
			attributes = []

			try:
				attributes = variables.split(';')				
			except Exception, e:
				print 'Error while parsing schema for relation ' + name
				print 'Line: ' + str(i + 1)
				sys.exit()

			schema = []
			for itm in attributes:
				try:
					p = itm.split(':')
					schema.append((p[0].strip(), p[1].strip()))
				except Exception, e:
					print 'Error while parsing schema for relation ' + name
					print 'Line: ' + str(i + 1)
					sys.exit()

			env[name] = schema
			runtime[name] = []


		if 'INSERT' in command:
			target_relation = parse[i][1].split()[2]

			if target_relation not in env:
				print 'Illegal insertion to an undefined relation ' + target_relation
				print 'Line: ' + str(i + 1)
				sys.exit()

			final = False
			new_parse = parse[i][1][parse[i][1].strip().index(target_relation) + len(target_relation):].strip()
			while not final:
				if ';' in new_parse:
					final = True
				else:
					print 'Error while parsing found EOF while expecting \';\' '
					print 'Line: ' + str(i + 1)
					sys.exit()

			new_parse = new_parse[:-1]
			
			if new_parse[0] != '(':				
				print 'Error while parsing insertion in ' + target_relation
				print 'Line: ' + str(i + 1)
				sys.exit()

			if new_parse[-1] != ')':				
				print 'Error while parsing insertion in ' + target_relation
				print 'Line: ' + str(i + 1)
				sys.exit()

			new_parse = new_parse[1:-1]
			new_parse = [_.strip() for _ in new_parse.split(',')]

			if len(new_parse) != len(env[target_relation]):								
				print 'Relation arity is: ' + str(len(target_relation))
				print 'Line: ' + str(i + 1)
				sys.exit()

			runtime[target_relation].append(new_parse)


		if i == len(parse) - 1:
			done = True

		i += 1

	return env

def set_runtime(env):

	for itm in env:
		name = itm
		types = []
		attributes = []
		for fields in env[itm]:
			attribute, burp_type = fields[0], fields[1]
			types.append(get_types(burp_type))
			attributes.append(attribute)
			

		rt_env[name] = Relation(name, types, attributes)
		add_fields(name, types, attributes)

def add_fields(name, types, attributes):
	obj = rt_env[name]
	records = runtime[name]
	
	for itm in records:
		
		i = 0
		tpl = []

		for atom in itm:

			expected_type = types[i]

			if str(expected_type(atom)) == 'NULL':				
				print 'Error while inserting ' + str(itm) + ' into ' +  name
				print 'Expected type was ' + str(expected_type)
				sys.exit()

			else:
				tpl.append(expected_type(atom))

			i += 1

		obj.insert(tpl)


def get_types(burp_type):
	if burp_type == 'BOOLEAN':
		return BOOL
	elif burp_type == 'INTEGER':
		return INT
	elif burp_type == 'REAL':
		return REAL
	elif burp_type == 'STRING':
		return STRING
	elif burp_type == 'CHAR':
		return CHAR
	elif burp_type == 'DATE':
		return DATE	

def main():
	filename = 'dml.burp'
	parse = parse_file(filename)
	env = set_env(parse)	
	set_runtime(env)

	for itm in rt_env:
		rt_env[itm].display()

if __name__ == '__main__':
	main()