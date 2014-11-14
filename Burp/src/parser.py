from pyparsing import OneOrMore, nestedExpr
inputdata = '(1 ((st 8) (pitch 67) (dur 4) (keysig 1) (timesig 12) (fermata 0))((st 12) (pitch 67) (dur 8) (keysig 1) (timesig 12) (fermata 0)))'
data = OneOrMore(nestedExpr()).parseString(inputdata)
print data