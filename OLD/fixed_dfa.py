#DFA. Every algorithmic function returns a tuple of (result, work).
#
#Cost model (same as my_dfa.py):
#  - reading a value (indexing, attribute access) costs 0
#  - each assignment costs 1 (including add/append/popleft, which write to a structure)
#  - each comparison / containment check (if, while condition, `in`) costs 1
#  - for-loop iteration bookkeeping is not counted

from collections import deque


class DFA:
    def __init__(self, num_states, num_symbols, delta, start, accepting):
        self.num_states = num_states
        self.num_symbols = num_symbols
        self.delta = delta #2D array with [state][symbol]
        self.start = start
        self.accepting = set(accepting) #set so the containment check is O(1)
        self.states = range(num_states) #each state is just a number
        self.alphabet = range(num_symbols) #each symbol is just a number

    #A single lookup: no assignment, no comparison -> 0 work.
    def step(self, q, symbol):
        return self.delta[q][symbol], 0

    #1 for the initial assignment of q, then 1 assignment per symbol.
    #Every assignment in the loop is used (the last one produces the returned state),
    #so nothing is subtracted. Work = len(word) + 1, which is >= 1 even for the empty word.
    #word is just an array of numbers
    def run(self, word, q=None):
        q = self.start if q is None else q
        work = 1
        for s in word:
            q = self.delta[q][s]
            work += 1
        return q, work

    #Work done to run the DFA, plus 1 for the assignment of the result
    #and 1 for the containment check. Work = len(word) + 3.
    def accepts(self, word):
        final, work = self.run(word)
        return (final in self.accepting), work + 2

    #BFS over reachable states. With R = number of reachable states, k = num_symbols:
    #  init (seen, queue)                     : 2
    #  while-condition checks                 : R + 1  (R true, 1 final false)
    #  popleft                                : R
    #  `if t not in seen` (once per edge)     : R*k
    #  add + append (once per new state)      : 2*(R - 1)
    #Total = R*k + 4R + 1
    def find_reachable(self):
        seen = {self.start}
        queue = deque([self.start])
        work = 2 #seen and queue initialization
        while True:
            work += 1 #while-condition check
            if not queue:
                break
            q = queue.popleft()
            work += 1 #popleft
            for t in self.delta[q]:
                work += 1 #the `if` containment check, done once per edge
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
                    work += 2 #add + append
        return seen, work

    #Display helpers: not algorithmic, so they return just a string.
    def stats_str(self):
        return (f"DFA(num_states={self.num_states}, num_symbols={self.num_symbols!r}, "
                f"start={self.start}, accepting={sorted(self.accepting)})")

    def table_str(self):
        names = [str(l) for l in self.states]
        w = max([len(n) for n in names] + [len(str(s)) for s in self.alphabet] + [5])
        header = "    " + "state".ljust(w) + " | " + " ".join(str(s).ljust(w) for s in self.alphabet)
        lines = [header, "-" * len(header)]
        for q in self.states:
            mark = ("->" if q == self.start else "  ") + ("*" if q in self.accepting else " ") + " "
            lines.append(mark + names[q].ljust(w) + " | "
                         + " ".join(names[t].ljust(w) for t in self.delta[q]))
        return "\n".join(lines)
