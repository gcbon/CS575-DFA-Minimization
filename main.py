"""Verify that the DFA class in dfa.py behaves correctly.

Run with:  python main.py
Exits with status 1 if any check fails.
"""

import random
import sys

from my_dfa import DFA
import work_functions

#num_states, num_symbols are constant for each problem
#delta, start, and accepting should have some impact on the problem
EXAMPLE = DFA(
    num_states=2,
    num_symbols=2,
    delta=[[0,1],
           [1,1]],
    start=0,
    accepting=set([0]),
    )

#running a character
print(EXAMPLE.step(0,0))

#running a word
print(EXAMPLE.run([0,0,1]))

#checking if a word accepts
print(EXAMPLE.run([0,0,1]))

#print details
print(EXAMPLE.stats_str())
print(EXAMPLE.table_str())

print(EXAMPLE.find_reachable())

#usage of work_functions
#work_functions return the amount of work required rather than the usual output
print(work_functions.find_reachable_work(EXAMPLE))
