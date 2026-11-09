#DFA. Every function returns a tuple of result, work

import random
from collections import deque


class DFA:
    def __init__(self, delta, start, accepting, num_states=None, num_symbols=None):
        self.num_states = num_states if num_states is not None else len(delta)
        self.num_symbols = num_symbols if num_symbols is not None else len(delta[0])
        self.delta = delta #2D array with [state][symbol]
        self.start = start
        self.accepting = accepting
        self.states = range(self.num_states) #each state is just a number
        self.alphabet = range(self.num_symbols) #each symbol is just a number

    #We consider accessing values to take 0 work, since there is no arithmetic or assignment
    def step(self, q, symbol):
        return self.delta[q][symbol]

    #Sum of assignments done in each loop. This is length of string. Subtract 1 because the last assignment isn't used.
    #word is just an arrays of numbers
    def run(self, word, q=None):
        q = self.start if q is None else q
        for s in word:
            q = self.step(q, s)
        return q

    #work done to run the DFA, followed by the assignment and containment check
    def accepts(self, word):
        final = self.run(word)
        return (final in self.accepting)

    def find_reachable(self):
        seen = {self.start}
        queue = deque([self.start])
        while queue:
            for t in self.delta[queue.popleft()]:
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
        return seen

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
