import sys

env = {}

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
					print 'Line: ' + str(j)
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
					print 'Line: ' + str(i)
					sys.exit()
				i += 1

			variables = variables.replace('{', '')
			attributes = []

			try:
				attributes = variables.split(';')				
			except Exception, e:
				print 'Error while parsing schema for relation ' + name
				print 'Line: ' + str(i)
				sys.exit()

			schema = []
			for itm in attributes:
				try:
					p = itm.split(':')
					schema.append((p[0].strip(), p[1].strip()))
				except Exception, e:
					print 'Error while parsing schema for relation ' + name
					print 'Line: ' + str(i)
					sys.exit()

			env[name] = schema


		if 'INSERT' in command:
			target_relation = parse[i][1].split()[2]

			if target_relation not in env:
				print 'Illegal insertion to an undefined relation ' + target_relation
				print 'Line: ' + str(i)
				sys.exit()

			j = i
			final = False
			new_parse = parse[parse[i][1].strip().index(target_relation) + len(target_relation):]
			print new_parse
			while not final:


				if ';' in parse[j][1]:
					final = True


		if i == len(parse) - 1:
			done = True

		i += 1



def main():
	filename = 'dml.burp'
	parse = parse_file(filename)
	set_env(parse)
	print env

if __name__ == '__main__':
	main()