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
    work += 2*len(word) #1 work for each assignment after the optional one and loop, minus last assignment to prevent double counting, plus final loop
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
        #1 work for loop overhead per reachable state + 1
        for t in DFA.delta[queue.popleft()]: #1 work for pop per reachable state
            #runs for every symbol x reachable state
            #1 work for loop overhead per symbol x reachable state + 1
            if t not in seen: #1 work per symbol x reachable state
                #runs for every reachable state
                seen.add(t) #1 work per reachable state
                queue.append(t) #1 work per reachable state
    work += 2*len(seen)*(DFA.num_symbols+1) + 4*len(seen) + 1
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
    work += 3*input_DFA.num_states - new_num_states + 1 #1 work for each state removed, 1 work to check, 1 work for loop overhead
    
    #input: old state number, output: new state number
    new_state_numbers = [-1 for i in range(input_DFA.num_states)]
    new_index = 0
    for old_index in reachable:
        new_state_numbers[old_index]=new_index
        new_index += 1
    #no work required since the mathematical definition doesn't need this step

    new_start = new_state_numbers[input_DFA.start]
    new_accepting = [new_state_numbers[i] for i in input_DFA.accepting if new_state_numbers[i]!=-1]
    work += 3*len(input_DFA.accepting) - len(new_accepting) + 1 #1 work for loop overhead, 1 work to check each item, 1 work to remove the items not present
    

    #first, remove unreachable rows
    new_delta = [row for i, row in enumerate(input_DFA.delta) if new_state_numbers[i]!=-1]
    work += 3*input_DFA.num_states - new_num_states + 1 #same justification as before
    #second, rename all states
    new_delta = [[new_state_numbers[i] for i in row] for row in new_delta]
    new_DFA = DFA(
        delta = new_delta,
        start = new_start,
        accepting= new_accepting
    )
    return new_DFA

def table_filling(input_DFA):
    global work
    num_states = input_DFA.num_states
    num_symbols = input_DFA.num_symbols
    accepting = input_DFA.accepting
    #first, initialize the table
    dependents = [[[] for _ in range(num_states)] for _ in range(num_states)]
    distinguish = [[None for _ in range(num_states)] for _ in range(num_states)]
    #we only need a triangular table, but it feels like a square would be easier?
    
    queue = deque()
    for p in range(num_states): #from 0 to num_states
        work += 1 #loop
        for q in range(p): #from 0 to p (don't bother with states outside the triangle)
            work += 1 #loop
            distinguish[p][q]=False
            for s in range(num_symbols):
                work += 1 #loop
                first = step(input_DFA, p, s) 
                second = step(input_DFA,q, s) 
                work += 2 #2 set insertions
                if first > second:
                    dependents[first][second].append((p,q))
                    work += 1 #append
                if first < second:
                    dependents[second][first].append((p,q))
                    work += 1 #append
                work += 1 #check
            work += 1 #loop end
            #set distinguish true if p and q have different accept values
            if (p in accepting) != (q in accepting):
                queue.append((p,q))
                work += 1 #append
            work+=3 #boolean expression
        work += 1 #loop end
    work += 1 #loop end

    #now we do the unraveling
    while queue:
        (p,q) = queue.popleft()
        work+=2 #loop and pop
        if not distinguish[p][q]:
            distinguish[p][q]=True
            work+=1 #set
            #only want to do this if we haven't already popped (p,q)
            for pair in dependents[p][q]:
                queue.append(pair)
                work += 2 #loop and append
            work += 1 #loop end
        work += 1 #check
    work += 1 #loop end
    return distinguish


#Myhill-Nerode minimization: remove unreachable states, then merge indistinguishable states
#work is not counted here yet (other than inside the helper functions)
def myhill_nerode(input_DFA):
    global work
    reachable_DFA = remove_unreachable(input_DFA)
    distinguish = table_filling(reachable_DFA)
    num_states = reachable_DFA.num_states

    #map each state to the smallest state equivalent to it (equivalence is transitive, so this is well defined)
    representative = list(range(num_states))
    for p in range(num_states):
        work += 1 #loop
        for q in range(p):
            work += 1 #loop
            if not distinguish[p][q]:
                representative[p] = representative[q]
                work += 1 #assignment
                break
            work += 1 #check
        work += 1 #loop end
    work += 1 #loop end
    #we will consider this to be the end of creating the equivalence class
    #all remaining work on that front will not be counted

    #number the equivalence classes 0..k-1
    new_state_numbers = [-1 for _ in range(num_states)]
    new_index = 0
    for p in range(num_states):
        if representative[p] == p:
            new_state_numbers[p] = new_index
            new_index += 1
    new_state_numbers = [new_state_numbers[representative[p]] for p in range(num_states)]

    #build the minimized DFA using each class's representative row
    new_delta = [[new_state_numbers[t] for t in reachable_DFA.delta[p]]
                 for p in range(num_states) if representative[p] == p]
    work += 2*len(reachable_DFA.delta) - len(new_delta) + 1 #1 work for each loop iteration, 1 work for each removal
    #renaming states doesn't count since that's only representational
    
    new_start = new_state_numbers[reachable_DFA.start]
    work += 1
    new_accepting = sorted({new_state_numbers[q] for q in reachable_DFA.accepting})
    work += len(reachable_DFA.delta) + 1 #1 work for each loop over the new states
    return DFA(
        delta = new_delta,
        start = new_start,
        accepting = new_accepting
    )


def myhill_nerode_work(input_DFA):
    global work
    reset_work()
    myhill_nerode(input_DFA)
    return work



#reverse a DFA into an NFA: every edge flipped, accepting states become start states, start becomes accepting
#returns (nfa_delta, starts, accepting) where nfa_delta[state][symbol] is a set of states
def reverse_dfa(input_DFA):
    global work
    nfa_delta = [[set() for _ in range(input_DFA.num_symbols)] for _ in range(input_DFA.num_states)]
    for q in range(input_DFA.num_states):
        for s in range(input_DFA.num_symbols):
            nfa_delta[input_DFA.delta[q][s]][s].add(q)
            work += 2
        work+=2
    return nfa_delta, set(input_DFA.accepting), {input_DFA.start}

#subset construction, only building subsets reachable from the start set
def determinize(nfa_delta, starts, accepting, num_symbols):
    global work
    start_set = frozenset(starts)
    subset_numbers = {start_set: 0}
    subsets = [start_set]
    new_delta = []
    queue = deque([start_set])
    while queue:
        work+=1 #loop
        current = queue.popleft()
        work += 1 #assignment used several times
        row = []
        for s in range(num_symbols):
            work += 1 #loop
            target = frozenset(t for q in current for t in nfa_delta[q][s])
            #not sure how much work this should count for
            if target not in subset_numbers:
                subset_numbers[target] = len(subsets)
                subsets.append(target)
                queue.append(target)
                work+=3
            work += 1 #containment check
            row.append(subset_numbers[target])
            work += 1
        work += 1 #loop end
        new_delta.append(row)
        work += 1
    work+=1 #loop end
    new_accepting = [i for i, subset in enumerate(subsets) if subset & accepting]
    return DFA(
        delta = new_delta,
        start = 0,
        accepting = new_accepting
    )

#Brzozowski's algorithm: determinize(reverse(determinize(reverse(DFA))))
def brzozowski(input_DFA):
    reversed_DFA = determinize(*reverse_dfa(input_DFA), input_DFA.num_symbols)
    return determinize(*reverse_dfa(reversed_DFA), input_DFA.num_symbols)
