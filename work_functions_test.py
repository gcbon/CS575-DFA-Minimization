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


#work_functions return the amount of work required rather than the usual output
print("work to find reachable states: ", work_functions.find_reachable_work(EXAMPLE))


#Note: anything after this isn't relevant to your work
print(work_functions.remove_unreachable(EXAMPLE).table_str())
print(work_functions.work)