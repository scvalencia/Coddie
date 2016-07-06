;; Save every single relation into a burp file
(SAVE (R1 ... Rn) 'object.burp')

;; Retrieves the relations from the burp file
(FETCH 'object.burp')

;; Inserts a new tuple into the relation
(INSERT (v1 ... vn) employee)

;; Deletes the given tuple from the relation
(DELETE (v1 ... vn) employee)

;; Assign to a new relation called as <name>, the result relation from <exp>
(SET <name> <exp>)

;; Returns the result reation from the union of relations r1 and r2
(UNION r1 r2)



(INSERT (v1 ... vn) (CREATE employee (name lastname salary) (STRING STRING INTEGER)))

(PRINT exp)

;; Projects a relation on the given argument
(PROJECT rel (a1 .. a2))


(GARBAGE name)
 ====================================

(create student (STRING STRING STRING REAL) (name lastname program gpa))
(insert student ("Daniel Lewis" "Karpis" "Computer Science" 3.7))

(display (project student (lastname program)))
(display student)

;; saves a single relation, given by an expression that evaluates to a relation
;; to a file named as filename given as a string "model.burp", if possible,
;; otherwise, it would report an appropiate error message

(save relation filename)

;; saves every relation in the enviroment to a file named as filename 
;; given as a string "model.burp", if possible, otherwise, it would 
;; report an appropiate error message

(save * filename)

;; saves every specified relation, given by several expressions that 
;; evaluates to relations to a file named as filename given as a string 
;; "model.burp", if possible, otherwise, it would report an appropiate 
;; error message

(save (relation1 relation2 ... relationn) filename)

;; exports the given relation using the specified option,
;; if option is "latex", it prints the LaTeX representation of the relation
;; if caption is given, it would be the caption of the LaTeX table. caption,
;; should be an string as in "This is a valid caption"
;; relation is an expression that evaluates to an expression

(export relation option caption?)



