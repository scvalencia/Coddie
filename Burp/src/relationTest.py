from relation import Relation
from dataTypes import INT
from dataTypes import STRING
from dataTypes import REAL

def date_model(number):

	# Relation suppliers: denotes suppliers under contract, each suplier has one
	# supplier number (SNO), which is unique; one name (SNAME), not necessarily 
	# unique, one rating or status (STATUS) and one location (CITY).

	name = 'Suppliers'
	types = [INT, STRING, INT, STRING]
	attributes = ['SNO', 'SNAME', 'STATUS', 'CITY']
	pk = 'SNO'
	suppliers = Relation(name, types, attributes, pk)

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

	# Relation parts: denotes kinds of parts. Each kind of part has one unique
	# part number (PNO), one name (PNAME), one color (COLOR), one weight (WEIGHT),
	# and one location where parts of that kind are stored.

	name = 'Parts'
	types = [INT, STRING, STRING, REAL, STRING]
	attributes = ['PNO', 'PNAME', 'COLOR', 'WEIGHT', 'CITY']
	pk = 'PNO'
	parts = Relation(name, types, attributes, pk)

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
	
	# Relation shipments: denotes shipments (which parts are supplied by which 
	# suppliers). Each shipment has one supplier number (SNO), one part number
	# (PNO), and one quantity (QTY).

	name = 'Shipments'
	types = [INT, INT, INT]
	attributes = ['SNO', 'PNO', 'QTY']
	pk = 'QTY'
	shipments = Relation(name, types, attributes, pk)

	data = (INT(1), INT(1), INT(300))
	shipments.insert(data)

	def test_string_rep():
		print
		print suppliers
		print 
		print parts
		print
		print shipments

	def menu(number):
		if number == 1:
			test_string_rep()

	menu(number)

date_model(1)
