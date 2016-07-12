;; saves a single relation to a file named as filename given as a string 
;; "model.burp" if possible. Otherwise, it would report an appropiate 
;; error message. relation must be an explicit relation

(save relation filename)

EXAMPLES:
	
	(save student "relations/student.burp")

;; saves every relation in the enviroment to a file named as filename 
;; given as a string "model.burp", if possible, otherwise, it would 
;; report an appropiate error message

(save * filename)

EXAMPLES:
	
	(save * "relations/student.burp")

;; saves every specified relation, given by several expressions that 
;; evaluates to relations to a file named as filename given as a string 
;; "model.burp", if possible, otherwise, it would report an appropiate 
;; error message

(save (relation1 relation2 ... relationn) filename)

EXAMPLES:
	
	(save (student employee) "relations/student.burp")

;; retreieves every single relation and populate them using the .burp file
;; specified in filename. It should have the form "model.burp", that is, an
;; string expression ending in '.burp'. If everything is properly setup, the 
;; action would be complete, and the enviroment is going to be populated from
;; those relations

(fetch filename)

EXAMPLES:
	
	(fetch "relations/student.burp")

;; displays a complete relation in the command line, specifying its attributes,
;; and whole data. relation should be an expression that evaluates 
;; to a relation, otherwise, the error would be shown. If the relation is 
;; not a relation in the enviroment, it would compute the relation and remove it
;; after the computation ends. It collects and throws the intermediate generated
;; relations

(display relation)

EXAMPLES:

	(display (project student (lastname program)))

	(display student)

	(display 
		(project 
			(project 
				employee 
				(name salary)
			) 
			(name)
		)
	)

	(display 
		(union 
			(project 
				(project 
					managers 
					(number surname)) 
				(number)) 
			(project graduates (number))))

;; exports the given relation using the specified option.
;;
;; if option is "latex", it prints the LaTeX representation of the relation
;; if caption is given, it would be the caption of the LaTeX table. caption,
;; should be an string as in "This is a valid caption".
;;
;; relation is an expression that evaluates to an expression
;; It collects and throws the intermediate generated relations

(export relation option caption?)

EXAMPLES:
	
	(export student "latex" "This is a relation")

	(export student "latex")

	(export 
		(project 
			(project 
				employee 
				(name salary)) 
			(name)) 
		"latex" 
		"This is a nice relation"
	)

;; displays the current database schema, that is, the current relations on 
;; the enviroment, and each schema.

(env)

;; end REPL execution

(exit)

;; creates a relation given its name, types and attributes. This command,
;; creates a new Relation object with schema name(attribute1:type1, ..., attributen:typen)
;; if the arity of types and attributes is the same, and you give a valid name, 
;; the operation would be successful. Otherwise, it would report an appropiate
;; error message. The computation of this stament, does evaluates to an empty
;; relation

(create name (type1 type2 ... typen) (attribute1 attribute2 ... attributen))

EXAMPLES:

	(create student (STRING STRING STRING REAL) (name lastname program gpa))

;; inserts a tuple in a relation. Given an existing relation (or on the fly created), 
;; and a tuple that satisfies the domain of the relation, it would add the new tuple to the 
;; existing relation. If the tuple does not fit the relation's arity, or its
;; domain; or the relation is not a valid relation, it would report an appropiate
;; error message. relation could also be an expression that evaluates to a relation

(insert relation (val1 val2 ... valn))

EXAMPLES:

	(insert            
		(create rel (STRING INTEGER) (name year))
		("Philip Flajolet" 1934))

	(insert 
		student 
		("Daniel Lewis" "Karpis" "Computer Science" 3.7))

	(insert 
		(project Movies (year)) 
		(3434))

;; produces from relation a new relation that has only some relation's columns.
;; Its value is a relation that has only the columns for attributes attri i = 1..n
;; The schema of the produced relation is the set of attributes {attr1 attr2 ... attrn},
;; which are shown in the order listed. relation is an expression that evaluates to a
;; relation, if any of the specified attributes does not belongs to the evaluated
;; relation attributes, or the relation expression does not evaluate to a valid relation
;; an error would be generated. The result relation, is added to the enviroment, with a
;; random name. It could be changed with the set operator
;; It collects and throws the intermediate generated relations

(project relation (attr1 attr2 ... attrn))

EXAMPLES:
	
	(project students (name gpa))

	(project 
		(project Movies (year length genre)) 
		(year genre))

;; select

EXAMPLES:

	(select employee (= name "ERNESTO"))

	(select 
		relation 
		(and 
			(= name "Pepito") 
			(<= age 45) 
			(or 
				(= religion "muslim") 
				(<> lastname "Curry")
			)))

	(select persons (not married))

	(select persons (<> religion "muslim"))

	(select 
		TuringAward 
		(and 
			(= firstname "Pepito") 
			(<= year 45) 
			(or 
				(= motivation "muslim") 
				(<> lastname "Knuth")
			)))

	(select 
			TuringAward 
			(or 
				(= lastname "Knuth")
				(= lastname "Perlis")
			))

	(select 
			TuringAward 
			(> year 1900))

;; produces an new relation from two relations, consisting in the set-union
;; of the tuples of the two original relations. It requieres type-compatibility,
;; and the schema of the resultign relation is the same as the first operand. That is
;; given (union relation1 reltion2), it evaluates to a relation with the same schema
;; as relation1. relation1, and relation2, must be expressions that evaluate to a 
;; relation, otherwise, an error would be raised. If the relations are not type-compatible,
;; an error would be raised. It collects and throws the intermediate generated relations.
;; The resulting relation, would be added to the enviroment

(union relation1 relation2)

EXAMPLES:
	
	(union managers graduates)

	(union 
		(project 
			(project managers (number surname)) 
			(number)) 
		(project graduates (number))
	)

;; produces an new relation from two relations, consisting in the set-intersection
;; of the tuples of the two original relations. It requieres type-compatibility,
;; and the schema of the resultign relation is the same as the first operand. That is
;; given (union relation1 reltion2), it evaluates to a relation with the same schema
;; as relation1. relation1, and relation2, must be expressions that evaluate to a 
;; relation, otherwise, an error would be raised. If the relations are not type-compatible,
;; an error would be raised. It collects and throws the intermediate generated relations.
;; The resulting relation, would be added to the enviroment

(inter relation1 relation2)

EXAMPLES:
	
	(inter managers graduates)

	(inter 
		(project 
			(project managers (number surname)) 
			(number)) 
		(project graduates (number))
	)

;; produces an new relation from two relations, consisting in the set-difference
;; of the tuples of the two original relations. It requieres type-compatibility,
;; and the schema of the resultign relation is the same as the first operand. That is
;; given (union relation1 reltion2), it evaluates to a relation with the same schema
;; as relation1. relation1, and relation2, must be expressions that evaluate to a 
;; relation, otherwise, an error would be raised. If the relations are not type-compatible,
;; an error would be raised. It collects and throws the intermediate generated relations.
;; The resulting relation, would be added to the enviroment

(diff relation1 relation2)

EXAMPLES:
	
	(diff managers graduates)

	(diff 
		(project 
			(project managers (number surname)) 
			(number)) 
		(project graduates (number))
	)