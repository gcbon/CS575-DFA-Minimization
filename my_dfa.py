#DFA. Every function returns a tuple of result, work

import random
from collections import deque


class DFA:
    def __init__(self, num_states, alphabet, delta, start, accepting):
        self.num_states = num_states
        self.alphabet = alphabet
        self.delta = delta #2D array with [state][symbol_id]
        self.start = start
        self.accepting = accepting
        self.states = range(num_states) #each state is just a number
        self._symbol_index = {s: i for i, s in enumerate(self.alphabet)} #assign a number to each letter

    #We consider accessing values to take 0 work, since there is no arithmetic or asssignment
    def step(self, q, symbol):
        return self.delta[q][self._symbol_index[symbol]]

    #Sum of assignments done in each loop. This is length of string. Subtract 1 because the last assignment isn't used.
    def run(self, word, q=None):
        q = self.start if q is None else q
        for s in word:
            q = self.step(q, s)
        return q, len(word)-1

    #work done to run the DFA, followed by the assignment and containment check
    def accepts(self, word):
        final, work = self.run(word)
        return (final in self.accepting), work+2

    def find_reachable(self):
        seen = {self.start}
        queue = deque([self.start])
        work = 2
        while queue:
            for t in self.delta[queue.popleft()]:
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
                    work += 2
                work += 1
        return seen, work

    def print_stats(self):
        return (f"DFA(num_states={self.num_states}, alphabet={self.alphabet!r}, "
                f"start={self.start}, accepting={sorted(self.accepting)})")

    def print_table(self):
        names = [str(l) for l in self.states]
        w = max([len(n) for n in names] + [len(str(s)) for s in self.alphabet] + [5])
        header = "    " + "state".ljust(w) + " | " + " ".join(str(s).ljust(w) for s in self.alphabet)
        lines = [header, "-" * len(header)]
        for q in self.states:
            mark = ("->" if q == self.start else "  ") + ("*" if q in self.accepting else " ") + " "
            lines.append(mark + names[q].ljust(w) + " | "
                         + " ".join(names[t].ljust(w) for t in self.delta[q]))
        return "\n".join(lines)
