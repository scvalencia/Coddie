from relation import Relation
from dataTypes import INT
from dataTypes import STRING
from dataTypes import REAL

def date_model(number):

	# As in Date- Databases in depth, pag 9

	# Relation suppliers: denotes suppliers under contract, each suplier has one
	# supplier number (SNO), which is unique; one name (SNAME), not necessarily 
	# unique, one rating or status (STATUS) and one location (CITY).

	name = 'Suppliers'
	types = [INT, STRING, INT, STRING]
	attributes = ['SNO', 'SNAME', 'STATUS', 'CITY']
	suppliers = Relation(name, types, attributes)

	# Relation parts: denotes kinds of parts. Each kind of part has one unique
	# part number (PNO), one name (PNAME), one color (COLOR), one weight (WEIGHT),
	# and one location where parts of that kind are stored.

	name = 'Parts'
	types = [INT, STRING, STRING, REAL, STRING]
	attributes = ['PNO', 'PNAME', 'COLOR', 'WEIGHT', 'CITY']
	parts = Relation(name, types, attributes)
	
	# Relation shipments: denotes shipments (which parts are supplied by which 
	# suppliers). Each shipment has one supplier number (SNO), one part number
	# (PNO), and one quantity (QTY).

	name = 'Shipments'
	types = [INT, INT, INT]
	attributes = ['SNO', 'PNO', 'QTY']
	shipments = Relation(name, types, attributes)

	name = 'Damage'
	types = [INT, STRING]
	attributes = ['SEX', 'NAME', 'LAST_NAME']
	dmg = Relation(name, types, attributes)

	def test_insert():		

		data = (INT(1), STRING('Smith'), INT(20), STRING('London'))
		suppliers.insert(data)

		data = (INT(2), STRING('Jones'), INT(10), STRING('Paris'))
		suppliers.insert(data)

		data = (INT(3), STRING('Blake'), INT(30), STRING('Paris'))
		suppliers.insert(data)

		data = (INT(4), STRING('Clark'), INT(20), STRING('London'))
		suppliers.insert(data)

		data = (INT(5), STRING('Adams'), INT(30), STRING('Athens'))
		suppliers.insert(data)

		print suppliers.error_queue

		data = (INT(1), STRING('Nut'), STRING('Red'), REAL(12.0), STRING('London'))
		parts.insert(data)

		data = (INT(2), STRING('Bolt'), STRING('Green'), REAL(17.0), STRING('Paris'))
		parts.insert(data)

		data = (INT(3), STRING('Screw'), STRING('Blue'), REAL(17.0), STRING('Oslo'))
		parts.insert(data)

		data = (INT(4), STRING('Screw'), STRING('Red'), REAL(14.0), STRING('London'))
		parts.insert(data)

		data = (INT(5), STRING('Cam'), STRING('Blue'), REAL(12.0), STRING('Paris'))
		parts.insert(data)

		data = (INT(6), STRING('Cog'), STRING('Red'), REAL(19.0), STRING('London'))
		parts.insert(data)

		print parts.error_queue

		data = (INT(1), INT(1), INT(300))
		shipments.insert(data)

		data = (INT(1), INT(2), INT(200))
		shipments.insert(data)

		data = (INT(1), INT(3), INT(400))
		shipments.insert(data)

		data = (INT(1), INT(4), INT(200))
		shipments.insert(data)

		data = (INT(1), INT(5), INT(100))
		shipments.insert(data)

		data = (INT(1), INT(6), INT(100))
		shipments.insert(data)

		data = (INT(2), INT(1), INT(300))
		shipments.insert(data)

		data = (INT(2), INT(2), INT(400))
		shipments.insert(data)

		data = (INT(3), INT(2), INT(200))
		shipments.insert(data)

		data = (INT(4), INT(2), INT(200))
		shipments.insert(data)

		data = (INT(4), INT(4), INT(300))
		shipments.insert(data)

		data = (INT(4), INT(5), INT(400))
		shipments.insert(data)

		data = (INT(4), INT(5), INT(400))
		shipments.insert(data)

		data = (INT(4), INT(5), REAL(400.0))
		shipments.insert(data)

		data = (INT(4), INT(5))
		shipments.insert(data)

		print shipments.error_queue

		suppliers.flush()
		parts.flush()
		shipments.flush()

	def test_display():
		print
		suppliers.display()
		print 
		parts.display()
		print
		shipments.display()

	def test_project():
		example = suppliers.project(['SNAME'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['NAME'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNO', 'SNAME'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNAME', 'SNO'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNAME', 'SNO', 'STATUS'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNAME', 'SNO', 'STATUS', 'CITY'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['city'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()		

		example = suppliers.project(['status'])
		if example:
			print example.name
			example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['NAME'])

		if example:
			example.display()

		print suppliers.error_queue
		suppliers.flush()

	def test_union():

		suppliers.flush()
		rigth = suppliers.project(['CITY'])

		if rigth:
			left = parts.project(['CITY'])
			union = rigth.union(left)

			if union:
				union.display()
				print union.error_queue

			print rigth.error_queue
			rigth.flush()

		example = suppliers.project(['CITY']).union(parts.project(['CITY']))
		example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNAME']).union(parts.project(['CITY']))
		example.display()

		print suppliers.error_queue
		suppliers.flush()

		rigth = suppliers.project(['SNO'])

		if rigth:
			left = parts.project(['CITY'])
			union = rigth.union(left)

			print rigth.error_queue
			rigth.flush()

	def test_cross():
		ans = suppliers.cross(parts)
		ans.display()

		ans = suppliers.project(['SNO', 'CITY']).cross(shipments)
		ans.display()

	def test_join():
		suppliers.join(shipments)

	def test_difference():

		name = 'Graduates'
		types = [INT, STRING, INT]
		attributes = ['NUMBER', 'SURNAME', 'AGE']
		t1 = Relation(name, types, attributes)

		data = (INT(7274), STRING('Robinson'), INT(37)); t1.insert(data)
		data = (INT(7432), STRING('Molley'), INT(39)); t1.insert(data)
		data = (INT(9824), STRING('Darkes'), INT(38)); t1.insert(data)


		name = 'Managers'
		types = [INT, STRING, INT]
		attributes = ['NUMBER', 'SURNAME', 'AGE']
		t2 = Relation(name, types, attributes)

		data = (INT(9297), STRING('Molley'), INT(56)); t2.insert(data)
		data = (INT(7432), STRING('Molley'), INT(39)); t2.insert(data)
		data = (INT(9824), STRING('Darkes'), INT(38)); t2.insert(data)

		
		diff = t1.diference(t2)
		diff.display()

		union = t1.union(t2)
		union.display()

		inter = t1.intersection(t2)
		inter.display()

		'''

		example = suppliers.project(['CITY']).union(parts.project(['CITY']))
		example.display()

		print suppliers.error_queue
		suppliers.flush()

		example = suppliers.project(['SNAME']).union(parts.project(['CITY']))
		example.display()

		print suppliers.error_queue
		suppliers.flush()

		rigth = suppliers.project(['SNO'])

		if rigth:
			left = parts.project(['CITY'])
			union = rigth.union(left)

			print rigth.error_queue
			rigth.flush()
		'''

	def menu(number):

		test_insert()

		if number == 1:
			test_display()

		elif number == 2:
			test_difference()

		elif number == 3:
			test_cross()

	menu(number)

date_model(2)
