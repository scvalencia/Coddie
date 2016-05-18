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

(CREATE employee (name lastname salary) (STRING STRING INTEGER))

(INSERT (v1 ... vn) (CREATE employee (name lastname salary) (STRING STRING INTEGER)))

(PRINT exp)

;; Projects a relation on the given argument
(PROJECT rel (a1 .. a2))



