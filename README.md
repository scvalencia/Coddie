# Coddie: An Interpreter for Extended Relational Algebra

Inspired by the simplicity and elegance of both the Scheme programming language, and the relational algebra formal system, Coddie is an interpreter with Lisp-like syntax that presents in a succint way a tool to study and explore relational algebra, as defined by E.F. Codd in his famous paper *A relational Model of Data for Large Shared Data Banks*, but extended in order to provite lighweight manipulation of data and data presentation.

This report describes the development and usage of Coddie. Coddie alows the user to define relations, to query them, and display them in appropiate forms. Now follows a description of  some examples of Coddie's capabilities.

### Coddie as Language for Data Modeling

Coddie is the combination of two very different parts, the first one, is the REPL, that provides an interface for interaction with the user; it offers a bridge between the relations, and the queries by the user. The second part, is the data modeling part, which allows definition of data, noth the structure and contents of relations, the former, can be done in the REPL, and in coddie files. Here is a description of both.

#### Coddie REPL

`REPL.py`

```
$ unix_workstation python Coddie/REPL.py

-----------	|	CODDIE - An Interpreter for Extended Relational Algebra
\         /	|	
 \       /	|	Documentation https://github.com/scvalencia/Coddie
  =======       |	Type "(help)" for help.
 /       \	|	
/         \	|	
-----------	|	Version 0.1.1 (2016-04-17)

>>>

```

Once the REPL is ready, it's possible to begin playing with the interactive relational algebra interpreter. The most basic operations to perfom, is to load a model that's properly described in a `codd` file. A file of this kind, has the description (mandatory) and the content (optional) of a relation. The description have both the attributes of a relation and its datatypes. The following file `model.codd`, describes two relations and the way to define them and populate them if needed. `codd` files, at the moment, are the only way to persist a querying session.

```sql
RELATION employee {
	nr : INTEGER
	name : STRING
	salary : INTEGER
}

INSERT (1, "John", 100) INTO employee

RELATION turingaward {
	firstname : STRING
	lastname : STRING
	year : INTEGER
	motivation : STRING
}

-- INSERT () INTO TuringAward
-- INSERT (1, 2, 3, 4) INTO TuringAward

INSERT ("Alan", "Perlis", 1966, "Compiler, construction") INTO turingaward
INSERT ("Alan", "Perlis", 1966, "Compiler, construction and, contributions") INTO turingaward

INSERT ("Maurice", "Wilkes", 1967, "Computer design and APIs") INTO turingaward
INSERT ("Richard", "Hamming", 1968, "Numerical methods and error correcting codes") INTO turingaward
INSERT ("Marvin", "Minsky", 1969, "AI research") INTO turingaward
INSERT ("James", "Wilkinson", 1970, "Numerical analysis in computation") INTO turingaward
INSERT ("John", "McCarthy", 1971, "AI research and LISP") INTO turingaward
INSERT ("Edsger", "Dijkstra", 1972, "Development of ALGOL, and the art of programming") INTO turingaward
```


$$\sigma_{(firstname\ =\ "Pepito")\ \wedge\ (year\ \leq\ 45)\ \wedge\ ((motivation\ =\ "muslim")\ \vee\ (lastname\ \neq\ "Knuth"))}\ (turingaward)$$