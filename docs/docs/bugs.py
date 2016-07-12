(display (select (cross sailors1 reserves) (= sid reserves.sid)))

Traceback (most recent call last):
  File "REPL.py", line 761, in <module>
    REPL()
  File "REPL.py", line 757, in REPL
    _eval(ast)
  File "REPL.py", line 598, in _eval
    _eval_io_instruction(query)
  File "REPL.py", line 273, in _eval_io_instruction
    return function_dct[command](query)
  File "REPL.py", line 204, in _display
    relation = _eval(query[1])
  File "REPL.py", line 604, in _eval
    return _eval_algebra_instruction(query)
  File "REPL.py", line 550, in _eval_algebra_instruction
    return function_dct[command](query)
  File "REPL.py", line 440, in _select
    if not _check_condition(relation, predicate): return
  File "REPL.py", line 106, in _check_condition
    return _check_atom(condition) == 0
  File "REPL.py", line 84, in _check_atom
    if not _check_attribute_value_type(relation, attribute, value_or_attribute):
  File "REPL.py", line 54, in _check_attribute_value_type
    if attribute_type != datatypes.infertype(value):
  File "/Users/scvalencia606/Documents/Programming/Python/Coddie/src/datatypes.py", line 198, in infertype
    if REAL(value).__str__() != 'NULL':
  File "/Users/scvalencia606/Documents/Programming/Python/Coddie/src/datatypes.py", line 99, in __str__
    if self.data:
AttributeError: 'REAL' object has no attribute 'data'


===========================================================================================


(display (select (cross sailors1 reserves) (= day "10/10/96")))

Error while creating relation sailors1_cross_reserves_9RGAXS. Types arity is 7, while attributes arity is 10
Traceback (most recent call last):
  File "REPL.py", line 761, in <module>
    REPL()
  File "REPL.py", line 757, in REPL
    _eval(ast)
  File "REPL.py", line 598, in _eval
    _eval_io_instruction(query)
  File "REPL.py", line 273, in _eval_io_instruction
    return function_dct[command](query)
  File "REPL.py", line 204, in _display
    relation = _eval(query[1])
  File "REPL.py", line 604, in _eval
    return _eval_algebra_instruction(query)
  File "REPL.py", line 550, in _eval_algebra_instruction
    return function_dct[command](query)
  File "REPL.py", line 436, in _select
    relation, predicate = _eval(query[1]), query[2]
  File "REPL.py", line 604, in _eval
    return _eval_algebra_instruction(query)
  File "REPL.py", line 550, in _eval_algebra_instruction
    return function_dct[command](query)
  File "REPL.py", line 526, in _cross
    resulting_relation  = this_relation.cross(that_relation)
  File "/Users/scvalencia606/Documents/Programming/Python/Coddie/src/relation.py", line 263, in cross
    that.tuples[that_tpl].data)
  File "/Users/scvalencia606/Documents/Programming/Python/Coddie/src/relation.py", line 77, in insert
    if t.arity != self.arity:
AttributeError: 'Relation' object has no attribute 'arity'