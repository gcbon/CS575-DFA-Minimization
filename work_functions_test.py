from my_dfa import DFA
import work_functions

deltafunc = [[0,1,2],
             [0,1,1],
             [0,1,1]]

EXAMPLE = DFA(
    delta=deltafunc,
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

#work_functions return the amount of work required rather than the usual output
print("work to find reachable states: ", work_functions.find_reachable_work(EXAMPLE))


#Note: anything after this isn't relevant to your work
#print(work_functions.remove_unreachable(EXAMPLE).table_str())
#print(work_functions.work)

print(work_functions.myhill_nerode(EXAMPLE).table_str())
print(work_functions.myhill_nerode_work(EXAMPLE))