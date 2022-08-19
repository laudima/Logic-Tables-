# Logic Tables

A program in python to automatically generate a truth table in from a logic preposition Latex and .tex. 

## How to use it ? 

To execute the program, run ```formulas.py``` from the terminal. 

1. To create a logic preposition, use the class _Formula_. 
2.First, declare your variables 

```
x1 = Formula(1) 
x2 = Formula(2) 

```
3. Use conjunctions, disjunctions and negations to form complex prepositions. 

```
x1 = Formula(1)
x2 = Formula(2)
x3 = Formula(3)
f1 = Formula(x1,'C',x2)
f2 = Formula(x3,'N')
f3 = Formula(f1, 'D', f2)

```
4.To create the table in Latex code use the function ```tabla_verdad()```
5.To generate the .tex file use the function  ```Latex(“name.tex”)```
