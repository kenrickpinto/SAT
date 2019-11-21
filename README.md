# SAT solver.

## Input format 
First line contains literals in csv format. 
Ex: If f = (a+b)(a+c)(a'+c). The first line will contain a,b,c. Do not include a' in this list.
The next few lines should contain clauses(one per line)

## Working

Function is initially analyzed for unit clauses. If found, the function is reduced.
The next step is finding pure literals and eliminating them by assigning appropriate values.

Once these are achieved, DPLL algorithm is recursively implemented to find a solution.
