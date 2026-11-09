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

#num_states and num_symbols can be inferred from delta (less error-prone)
EXAMPLE = DFA(
    delta=[[0,1],
           [1,1]],
    start=0,
    accepting=set([0]),
    )

#running a character
print("running DFA with character 0: ", EXAMPLE.step(0,0))

#running a word
print("running DFA with word 001: ", EXAMPLE.run([0,0,1]))

#checking if a word accepts
print("checking for acceptance with word 001: ", EXAMPLE.accepts([0,0,1]))

#print details
print(EXAMPLE.stats_str())
print(EXAMPLE.table_str())

print("reachable states: ", EXAMPLE.find_reachable())

#usage of work_functions
#work_functions return the amount of work required rather than the usual output
print("work to find reachable states: ", work_functions.find_reachable_work(EXAMPLE))
