"""Deterministic finite automaton representation suited to minimization algorithms.

States are stored internally as integers ``0 .. n-1`` and symbols as integers
``0 .. k-1`` so that the transition function is a dense ``n x k`` table. That
layout makes the operations minimization algorithms need (refining partitions,
computing preimages, building quotient automata) simple and fast. Original
state and symbol labels are kept so results can be shown in readable form.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Dict, Hashable, Iterable, List, Optional, Sequence, Set, Tuple


class DFA:
    """A complete deterministic finite automaton.

    Attributes:
        num_states:   number of states ``n``; states are ``0 .. n-1``.
        alphabet:     tuple of symbol labels; symbol ``i`` is ``alphabet[i]``.
        delta:        ``delta[q][a]`` is the state reached from ``q`` on symbol index ``a``.
        start:        start state index.
        accepting:    frozenset of accepting state indices.
        state_labels: optional readable name for each state index.
    """

    __slots__ = ("num_states", "alphabet", "delta", "start", "accepting",
                 "state_labels", "_symbol_index", "_inverse")

    def __init__(
        self,
        num_states: int,
        alphabet: Sequence[Hashable],
        delta: Sequence[Sequence[int]],
        start: int,
        accepting: Iterable[int],
        state_labels: Optional[Sequence[Hashable]] = None,
    ) -> None:
        self.num_states = num_states
        self.alphabet = tuple(alphabet)
        self.delta = [list(row) for row in delta]
        self.start = start
        self.accepting = frozenset(accepting)
        self.state_labels = (list(state_labels) if state_labels is not None
                             else list(range(num_states)))
        self._symbol_index = {s: i for i, s in enumerate(self.alphabet)}
        self._inverse: Optional[List[List[List[int]]]] = None
        self._validate()

    # ------------------------------------------------------------------ #
    # Construction helpers
    # ------------------------------------------------------------------ #
    @classmethod
    def from_transitions(
        cls,
        states: Iterable[Hashable],
        alphabet: Iterable[Hashable],
        transitions: Dict[Tuple[Hashable, Hashable], Hashable],
        start: Hashable,
        accepting: Iterable[Hashable],
        complete: bool = True,
    ) -> "DFA":
        """Build a DFA from labelled states and a ``{(state, symbol): state}`` dict.

        If ``complete`` is True, missing transitions are routed to a new dead
        (trap) state. Otherwise every transition must be defined.
        """
        states = list(states)
        alphabet = list(alphabet)
        idx = {s: i for i, s in enumerate(states)}
        if len(idx) != len(states):
            raise ValueError("duplicate state labels")
        sym = {a: i for i, a in enumerate(alphabet)}
        if len(sym) != len(alphabet):
            raise ValueError("duplicate alphabet symbols")

        dead = len(states)
        delta: List[List[int]] = []
        for q in states:
            row = []
            for a in alphabet:
                target = transitions.get((q, a))
                if target is None:
                    raise ValueError(f"missing transition for ({q!r}, {a!r})")                    
                else:
                    if target not in idx:
                        raise ValueError(f"unknown target state {target!r}")
                    row.append(idx[target])
            delta.append(row)

        for (q, a) in transitions:
            if q not in idx or a not in sym:
                raise ValueError(f"transition on unknown state/symbol ({q!r}, {a!r})")

        labels: List[Hashable] = list(states)

        return cls(len(labels), alphabet, delta, idx[start],
                   (idx[q] for q in accepting), labels)

    @classmethod
    def random(
        cls,
        num_states: int,
        alphabet: Sequence[Hashable] = ("0", "1"),
        accept_prob: float = 0.5,
        rng: Optional[random.Random] = None,
    ) -> "DFA":
        """Generate a random complete DFA (useful for testing and benchmarks)."""
        rng = rng or random.Random()
        k = len(alphabet)
        delta = [[rng.randrange(num_states) for _ in range(k)] for _ in range(num_states)]
        accepting = [q for q in range(num_states) if rng.random() < accept_prob]
        return cls(num_states, alphabet, delta, 0, accepting)

    def copy(self) -> "DFA":
        return DFA(self.num_states, self.alphabet, self.delta, self.start,
                   self.accepting, self.state_labels)

    def _validate(self) -> None:
        n, k = self.num_states, len(self.alphabet)
        if n < 1:
            raise ValueError("a DFA needs at least one state")
        if len(self.delta) != n:
            raise ValueError("delta must have one row per state")
        if len(self.state_labels) != n:
            raise ValueError("state_labels must have one entry per state")
        if not 0 <= self.start < n:
            raise ValueError("start state out of range")
        for q, row in enumerate(self.delta):
            if len(row) != k:
                raise ValueError(f"state {q} has {len(row)} transitions, expected {k}")
            for t in row:
                if not 0 <= t < n:
                    raise ValueError(f"transition from state {q} to out-of-range state {t}")
        for q in self.accepting:
            if not 0 <= q < n:
                raise ValueError(f"accepting state {q} out of range")

    # ------------------------------------------------------------------ #
    # Basic queries
    # ------------------------------------------------------------------ #
    @property
    def states(self) -> range:
        return range(self.num_states)

    @property
    def num_symbols(self) -> int:
        return len(self.alphabet)

    def symbol_index(self, symbol: Hashable) -> int:
        return self._symbol_index[symbol]

    def is_accepting(self, q: int) -> bool:
        return q in self.accepting

    def step(self, q: int, symbol: Hashable) -> int:
        """Transition on a symbol label."""
        return self.delta[q][self._symbol_index[symbol]]

    def run(self, word: Iterable[Hashable], q: Optional[int] = None) -> int:
        """Return the state reached after reading ``word`` from ``q`` (default: start)."""
        q = self.start if q is None else q
        for s in word:
            q = self.delta[q][self._symbol_index[s]]
        return q

    def accepts(self, word: Iterable[Hashable]) -> bool:
        return self.run(word) in self.accepting

    # ------------------------------------------------------------------ #
    # Structures used by minimization algorithms
    # ------------------------------------------------------------------ #
    def inverse(self) -> List[List[List[int]]]:
        """``inverse()[a][q]`` lists every state ``p`` with ``delta[p][a] == q``.

        Hopcroft's algorithm uses this to find the preimage of a splitter
        block. The result is cached; treat it as read-only.
        """
        if self._inverse is None:
            inv = [[[] for _ in range(self.num_states)] for _ in range(self.num_symbols)]
            for p, row in enumerate(self.delta):
                for a, q in enumerate(row):
                    inv[a][q].append(p)
            self._inverse = inv
        return self._inverse

    def preimage(self, block: Iterable[int], a: int) -> Set[int]:
        """States that move into ``block`` on symbol index ``a``."""
        inv_a = self.inverse()[a]
        result: Set[int] = set()
        for q in block:
            result.update(inv_a[q])
        return result

    def initial_partition(self) -> List[Set[int]]:
        """The accepting / non-accepting split (empty blocks omitted)."""
        acc = set(self.accepting)
        rej = set(self.states) - acc
        return [b for b in (acc, rej) if b]

    def reachable_states(self) -> Set[int]:
        """States reachable from the start state (BFS)."""
        seen = {self.start}
        queue = deque([self.start])
        while queue:
            q = queue.popleft()
            for t in self.delta[q]:
                if t not in seen:
                    seen.add(t)
                    queue.append(t)
        return seen

    def remove_unreachable(self) -> "DFA":
        """Return an equivalent DFA with unreachable states removed.

        Surviving states are renumbered in BFS order from the start state.
        """
        order: List[int] = [self.start]
        new_id = {self.start: 0}
        i = 0
        while i < len(order):
            for t in self.delta[order[i]]:
                if t not in new_id:
                    new_id[t] = len(order)
                    order.append(t)
            i += 1
        delta = [[new_id[t] for t in self.delta[q]] for q in order]
        accepting = [new_id[q] for q in order if q in self.accepting]
        labels = [self.state_labels[q] for q in order]
        return DFA(len(order), self.alphabet, delta, 0, accepting, labels)

    def quotient(self, partition: Iterable[Iterable[int]]) -> "DFA":
        """Build the DFA whose states are the blocks of ``partition``.

        ``partition`` must cover every state and be a congruence (states in a
        block go to the same block on each symbol), which is exactly what a
        minimization algorithm produces. Blocks are renumbered in BFS order
        from the start block so equal languages give identical outputs.
        """
        blocks = [sorted(b) for b in partition if b]
        block_of = [-1] * self.num_states
        for i, b in enumerate(blocks):
            for q in b:
                if block_of[q] != -1:
                    raise ValueError(f"state {q} appears in more than one block")
                block_of[q] = i
        if -1 in block_of:
            raise ValueError(f"state {block_of.index(-1)} is not in any block")

        raw_delta = []
        for b in blocks:
            rep = b[0]
            row = [block_of[t] for t in self.delta[rep]]
            for q in b[1:]:
                if [block_of[t] for t in self.delta[q]] != row:
                    raise ValueError("partition is not compatible with the transitions")
            raw_delta.append(row)
        raw_acc = [i for i, b in enumerate(blocks) if b[0] in self.accepting]
        labels = [frozenset(self.state_labels[q] for q in b) for b in blocks]

        return DFA(len(blocks), self.alphabet, raw_delta, block_of[self.start],
                   raw_acc, labels).remove_unreachable()

    # ------------------------------------------------------------------ #
    # Comparison
    # ------------------------------------------------------------------ #
    def equivalent(self, other: "DFA") -> Tuple[bool, Optional[Tuple[Hashable, ...]]]:
        """Check whether two DFAs accept the same language.

        Explores the product automaton by BFS. Returns ``(True, None)`` if
        equivalent, otherwise ``(False, w)`` where ``w`` is a shortest word
        accepted by exactly one of them.
        """
        if set(self.alphabet) != set(other.alphabet):
            raise ValueError("DFAs have different alphabets")
        other_sym = [other._symbol_index[s] for s in self.alphabet]
        start = (self.start, other.start)
        parent: Dict[Tuple[int, int], Optional[Tuple[Tuple[int, int], int]]] = {start: None}
        queue = deque([start])
        while queue:
            p, q = queue.popleft()
            if (p in self.accepting) != (q in other.accepting):
                word: List[Hashable] = []
                node = (p, q)
                while parent[node] is not None:
                    node, a = parent[node]
                    word.append(self.alphabet[a])
                return False, tuple(reversed(word))
            for a in range(self.num_symbols):
                nxt = (self.delta[p][a], other.delta[q][other_sym[a]])
                if nxt not in parent:
                    parent[nxt] = ((p, q), a)
                    queue.append(nxt)
        return True, None

    def is_isomorphic(self, other: "DFA") -> bool:
        """True if the reachable parts are identical up to state renaming."""
        if set(self.alphabet) != set(other.alphabet):
            return False
        a, b = self.remove_unreachable(), other.remove_unreachable()
        if a.num_states != b.num_states:
            return False
        perm = [b._symbol_index[s] for s in a.alphabet]
        b_delta = [[row[perm[i]] for i in range(a.num_symbols)] for row in b.delta]
        # BFS renumbering only depends on symbol order, which we aligned above.
        b_aligned = DFA(b.num_states, a.alphabet, b_delta, b.start, b.accepting).remove_unreachable()
        return a.delta == b_aligned.delta and a.accepting == b_aligned.accepting

    # ------------------------------------------------------------------ #
    # Display
    # ------------------------------------------------------------------ #
    def __len__(self) -> int:
        return self.num_states

    def __repr__(self) -> str:
        return (f"DFA(num_states={self.num_states}, alphabet={self.alphabet!r}, "
                f"start={self.start}, accepting={sorted(self.accepting)})")

    def __str__(self) -> str:
        def fmt(label: Hashable) -> str:
            if isinstance(label, frozenset):
                return "{" + ",".join(sorted(fmt(x) for x in label)) + "}"
            return str(label)

        names = [fmt(l) for l in self.state_labels]
        w = max([len(n) for n in names] + [len(str(s)) for s in self.alphabet] + [5])
        header = " " * 4 + "state".ljust(w) + " | " + " ".join(str(s).ljust(w) for s in self.alphabet)
        lines = [header, "-" * len(header)]
        for q in self.states:
            mark = ("->" if q == self.start else "  ") + ("*" if q in self.accepting else " ") + " "
            lines.append(mark + names[q].ljust(w) + " | "
                         + " ".join(names[t].ljust(w) for t in self.delta[q]))
        return "\n".join(lines)
