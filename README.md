# ConCloAlg
A simple implementation of the Congruence Closure Algorithm used to decide the satisfiablity of formulas in the quantifier-free theory of equality.

## Installation

1. Create a virtual environment from the 'requirements.txt' file.
2. Done.

### Testing

To test the algorithm and its sub-functions run 'test.py'. This will also generate a coverage report.

## Running

As of right now, the DAG has to be created manually. Edit the file 'run.py' (examples are included):

1. Add nodes for the DAG
2. Set the nodes' arguments.
3. Create two lists:
   * A merge list for all equalities.
   * An inequalities list that will be used to check the formula's satisfiability.
