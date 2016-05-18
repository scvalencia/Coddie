import relation

# Set operators

def union(r1, r2):
	return r1.union(r2)

def intersection(r1, r2):
	return r1.intersection(r2)

def difference(r1, r2):
	return r1.difference(r2)

def cross(r1, r2):
	return r1.cross(r2)

# Relational operators

def project(r1, attributes):
	return r1.project(attributes)

def select(r1, foo):
	return r1.select(foo)

def join(r1, r2):
	return r1.join(r2)