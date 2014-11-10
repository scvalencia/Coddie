from dbTypes import *

__author__ = 'scvalencia'

class relation(object):
    def __init__(self, name, ):
        pass

yr = dbTypes.YEAR(2011)
nt = dbTypes.INT(3)
st = dbTypes.STRING('SEBASTIAN_VALENCIA')
ch = dbTypes.CHAR('a')
db = dbTypes.DOUBLE(123123213.1231231)
dt = dbTypes.DATE('2011-09-21 15:31:54')
bl = dbTypes.BOOL('FALSE')
nm = dbTypes.ENUM('Day', ['STRING', 'STRING', 'INT'], ['MONDAY', 'FRIDAY', 2])
print yr, nt, st, ch, db, dt, bl
print nm
