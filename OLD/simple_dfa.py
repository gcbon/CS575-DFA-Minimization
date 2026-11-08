"""A minimal DFA class: states are 0..n-1, symbols are indexed into a dense table.

No input validation or error handling -- inputs are assumed to be well formed.
"""

import random
from collections import deque


class DFA:
    def __init__(self, num_states, alphabet, delta, start, accepting):
        self.num_states = num_states
        self.alphabet = tuple(alphabet)
        self.delta = [list(row) for row in delta]
        self.start = start
        self.accepting = frozenset(accepting)
        self.state_labels = list(range(num_states))
        self._symbol_index = {s: i for i, s in enumerate(self.alphabet)}

    @classmethod
    def from_transitions(cls, states, alphabet, transitions, start, accepting):
        """Build a DFA from labelled states and a {(state, symbol): state} dict."""
        states = list(states)
        alphabet = list(alphabet)
        idx = {s: i for i, s in enumerate(states)}
        delta = [[idx[transitions[(q, a)]] for a in alphabet] for q in states]
        return cls(len(states), alphabet, delta, idx[start],
                   [idx[q] for q in accepting], states)

    @classmethod
    def random(cls, num_states, alphabet=("0", "1"), accept_prob=0.5, rng=None):
        """Generate a random complete DFA."""
        rng = rng or random.Random()
        delta = [[rng.randrange(num_states) for _ in alphabet] for _ in range(num_states)]
        accepting = [q for q in range(num_states) if rng.random() < accept_prob]
        return cls(num_states, alphabet, delta, 0, accepting)

    @property
    def states(self):
        return range(self.num_states)

    def step(self, q, symbol):
        return self.delta[q][self._symbol_index[symbol]]

    def run(self, word, q=None):
        q = self.start if q is None else q
        for s in word:
            q = self.step(q, s)
        return q

    def accepts(self, word):
        return self.run(word) in self.accepting

    def reachable_states(self):
        seen = {self.start}
        queue = deque([self.start])
        while queue:
            for t in self.delta[queue.popleft()]:
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
        return seen

    def __len__(self):
        return self.num_states

    def __repr__(self):
        return (f"DFA(num_states={self.num_states}, alphabet={self.alphabet!r}, "
                f"start={self.start}, accepting={sorted(self.accepting)})")

    def __str__(self):
        names = [str(l) for l in self.state_labels]
        w = max([len(n) for n in names] + [len(str(s)) for s in self.alphabet] + [5])
        header = "    " + "state".ljust(w) + " | " + " ".join(str(s).ljust(w) for s in self.alphabet)
        lines = [header, "-" * len(header)]
        for q in self.states:
            mark = ("->" if q == self.start else "  ") + ("*" if q in self.accepting else " ") + " "
            lines.append(mark + names[q].ljust(w) + " | "
                         + " ".join(names[t].ljust(w) for t in self.delta[q]))
        return "\n".join(lines)
