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
    work += len(word)-1 #1 work for each assignment after the optional one, minus last assignment to prevent double counting
    return DFA.run(word,q)


def accept(DFA, word):
    global work
    final = run(DFA, word)
    work += 2 #assignment plus membership check
    return (final in DFA.accepting)

#1 work for each add to seen and queue, 1 work for each removal
#You do 3 work for each item added to the queue and 2 work for every unique item added    
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