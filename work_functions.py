from my_dfa import DFA
from collections import deque
work = 0

def reset_work():
    global work
    work = 0

#0 work for an abstract lookup, assignment will be computed later
def step(DFA, q, symbol):
    global work
    work += 0
    return DFA.delta[q][symbol]

def run(DFA, word, q=None):
    global work
    work += 2*len(word)-1 #1 work for each assignment after the optional one and loop, minus last assignment to prevent double counting
    return DFA.run(word,q)


def accept(DFA, word):
    global work
    final = run(DFA, word)
    work += 2 #assignment plus membership check
    return (final in DFA.accepting)

#1 work for each add to seen and queue, 1 work for each removal
def find_reachable(DFA):
    global work
    seen = {DFA.start}
    queue = deque([DFA.start])
    #work = 2
    while queue:
        #runs for every reachable state
        #1 work for loop overhead per reachable state
        for t in DFA.delta[queue.popleft()]: #1 work for pop per reachable state
            #runs for every symbol x reachable state 
            #1 work for loop overhead per symbol x reachable state
            if t not in seen: #1 work per symbol x reachable state
                #runs for every reachable state
                seen.add(t) #1 work per reachable state
                queue.append(t) #1 work per reachable state
    work += 2*len(seen)*(DFA.num_symbols) + 4*len(seen)
    return seen

def find_reachable_work(DFA):
    global work
    reset_work()
    find_reachable(DFA)
    return work

#here, the count of work assumes everything is done in-place, as that is the mathematically fastest way to do it
def remove_unreachable(input_DFA):
    global work
    reachable = find_reachable(input_DFA)
    new_num_symbols = input_DFA.num_symbols
    new_num_states = len(reachable)
    work += 3*input_DFA.num_states - new_num_states #1 work for each state removed, 1 work to check, 1 work for loop overhead
    
    #input: old state number, output: new state number
    new_state_numbers = [-1 for i in range(input_DFA.num_states)]
    new_index = 0
    for old_index in reachable:
        new_state_numbers[old_index]=new_index
        new_index += 1
    #no work required since the mathematical definition doesn't need this step

    new_start = new_state_numbers[input_DFA.start]
    new_accepting = [new_state_numbers[i] for i in input_DFA.accepting if new_state_numbers[i]!=-1]
    work += 3*len(input_DFA.accepting) - len(new_accepting) #1 work for loop overhead, 1 work to check each item, 1 work to remove the items not present
    

    #first, remove unreachable rows
    new_delta = [row for i, row in enumerate(input_DFA.delta) if new_state_numbers[i]!=-1]
    work += 3*input_DFA.num_states - new_num_states #same justification as before
    #second, rename all states
    new_delta = [[new_state_numbers[i] for i in row] for row in new_delta]
    new_DFA = DFA(
        new_num_states,
        new_num_symbols,
        new_delta,
        new_start,
        new_accepting
    )
    return new_DFA