"""Verify that the DFA class in dfa.py behaves correctly.

Run with:  python main.py
Exits with status 1 if any check fails.
"""

import random
import sys

from dfa import DFA

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")


def raises(fn, exc=ValueError):
    try:
        fn()
    except exc:
        return True
    return False


def moore_minimize(d):
    """Reference Moore minimization, used to exercise the minimization helpers."""
    d = d.remove_unreachable()
    partition = d.initial_partition()
    while True:
        block_of = {q: i for i, b in enumerate(partition) for q in b}
        groups = {}
        for q in d.states:
            sig = (block_of[q],) + tuple(block_of[t] for t in d.delta[q])
            groups.setdefault(sig, set()).add(q)
        refined = list(groups.values())
        if len(refined) == len(partition):
            return d.quotient(refined)
        partition = refined


def brute_force_equal(a, b, max_len=6):
    """Compare two DFAs on every word up to max_len (independent of DFA.equivalent)."""
    words = [()]
    for _ in range(max_len + 1):
        for w in words:
            if a.accepts(w) != b.accepts(w):
                return False
        words = [w + (s,) for w in words for s in a.alphabet]
    return True


# --------------------------------------------------------------------------- #
# Example: binary strings with exactly one "1" (0*10*), built with redundant states.
# --------------------------------------------------------------------------- #
EXAMPLE = DFA.from_transitions(
    states="ABCDEF",
    alphabet="01",
    transitions={
        ("A", "0"): "B", ("A", "1"): "C",
        ("B", "0"): "A", ("B", "1"): "D",
        ("C", "0"): "E", ("C", "1"): "F",
        ("D", "0"): "E", ("D", "1"): "F",
        ("E", "0"): "E", ("E", "1"): "F",
        ("F", "0"): "F", ("F", "1"): "F",
    },
    start="A",
    accepting="CDE",
)


def test_construction():
    print("Construction & validation")
    check("example has 6 states", EXAMPLE.num_states == 6)
    check("alphabet preserved", EXAMPLE.alphabet == ("0", "1"))
    check("start state is A", EXAMPLE.state_labels[EXAMPLE.start] == "A")

    partial = DFA.from_transitions("ab", "x", {("a", "x"): "b"}, "a", "b")
    check("missing transitions add a dead state", partial.num_states == 3
          and partial.state_labels[2] == "_dead")
    check("dead state loops to itself", partial.delta[2] == [2])

    check("complete=False rejects missing transitions", raises(
        lambda: DFA.from_transitions("ab", "x", {("a", "x"): "b"}, "a", "b", complete=False)))
    check("unknown target state rejected", raises(
        lambda: DFA.from_transitions("a", "x", {("a", "x"): "z"}, "a", "")))
    check("out-of-range transition rejected", raises(
        lambda: DFA(2, "01", [[0, 1], [0, 5]], 0, [])))
    check("wrong row length rejected", raises(
        lambda: DFA(2, "01", [[0, 1], [0]], 0, [])))
    check("bad start state rejected", raises(
        lambda: DFA(1, "0", [[0]], 3, [])))
    check("bad accepting state rejected", raises(
        lambda: DFA(1, "0", [[0]], 0, [4])))
    check("zero states rejected", raises(lambda: DFA(0, "0", [], 0, [])))

    c = EXAMPLE.copy()
    c.delta[0][0] = 5
    check("copy is independent of original", EXAMPLE.delta[0][0] != 5)


def test_acceptance():
    print("Running words")
    cases = {"": False, "1": True, "01": True, "00": False, "001": True,
             "10": True, "11": False, "0001": True, "110": False, "0101": False}
    for word, expected in cases.items():
        check(f"accepts({word!r}) == {expected}", EXAMPLE.accepts(word) == expected)
    check("step uses symbol labels", EXAMPLE.step(0, "1") == 2)
    check("run from a given state", EXAMPLE.run("0", q=2) == 4)
    check("unknown symbol raises KeyError", raises(lambda: EXAMPLE.accepts("2"), KeyError))


def test_minimization_helpers():
    print("Minimization helpers")
    part = EXAMPLE.initial_partition()
    check("initial partition is accepting / rejecting",
          sorted(map(sorted, part)) == [[0, 1, 5], [2, 3, 4]])

    inv = EXAMPLE.inverse()
    ok = all(EXAMPLE.delta[p][a] == q
             for a in range(EXAMPLE.num_symbols)
             for q in EXAMPLE.states
             for p in inv[a][q])
    count = sum(len(inv[a][q]) for a in range(2) for q in EXAMPLE.states)
    check("inverse() matches delta", ok and count == 6 * 2)
    check("preimage of {F} on '1'", EXAMPLE.preimage({5}, 1) == {2, 3, 4, 5})

    unreachable = DFA(4, "ab", [[1, 1], [0, 0], [3, 0], [2, 2]], 0, [1, 3])
    check("reachable_states finds {0,1}", unreachable.reachable_states() == {0, 1})
    trimmed = unreachable.remove_unreachable()
    check("remove_unreachable drops states", trimmed.num_states == 2)
    check("remove_unreachable keeps language", unreachable.equivalent(trimmed)[0])

    m = moore_minimize(EXAMPLE)
    check("example minimizes to 3 states", m.num_states == 3)
    check("minimized DFA is equivalent", EXAMPLE.equivalent(m)[0])
    check("minimized DFA agrees on all short words", brute_force_equal(EXAMPLE, m))
    check("quotient labels merge original states",
          set(m.state_labels) == {frozenset("AB"), frozenset("CDE"), frozenset("F")})

    check("quotient rejects overlapping blocks", raises(
        lambda: EXAMPLE.quotient([{0, 1}, {1, 2, 3, 4, 5}])))
    check("quotient rejects missing states", raises(
        lambda: EXAMPLE.quotient([{0, 1}, {2, 3, 4}])))
    check("quotient rejects incompatible partition", raises(
        lambda: EXAMPLE.quotient([{0, 2}, {1, 3, 4}, {5}])))


def test_comparison():
    print("Equivalence & isomorphism")
    a = DFA(2, "01", [[1, 1], [1, 1]], 0, [1])
    b = DFA(2, "01", [[1, 1], [0, 0]], 0, [1])
    eq, witness = a.equivalent(b)
    check("non-equivalent DFAs detected", not eq)
    check("counterexample really distinguishes them",
          witness is not None and a.accepts(witness) != b.accepts(witness))
    check("counterexample is shortest (length 2)", witness is not None and len(witness) == 2)

    # Same machine as EXAMPLE's minimum, but with states and symbols reordered:
    # state 0 = dead, 1 = start (no 1 seen), 2 = one 1 seen; column 0 is '1'.
    renamed = DFA(3, "10", [[0, 0], [2, 1], [0, 2]], 1, [2])
    m = moore_minimize(EXAMPLE)
    check("renamed minimal DFA is equivalent", m.equivalent(renamed)[0])
    check("renamed minimal DFA is isomorphic", m.is_isomorphic(renamed))
    check("non-minimal DFA is not isomorphic to minimal", not EXAMPLE.is_isomorphic(m))
    check("different alphabets raise", raises(
        lambda: a.equivalent(DFA(1, "ab", [[0, 0]], 0, []))))


def test_random(trials=500, seed=575):
    print(f"Randomized checks ({trials} random DFAs)")
    rng = random.Random(seed)
    ok_equiv = ok_size = ok_idem = ok_brute = True
    for _ in range(trials):
        d = DFA.random(rng.randint(1, 12), "abc", rng=rng)
        m = moore_minimize(d)
        ok_equiv &= d.equivalent(m)[0]
        ok_size &= m.num_states <= len(d.reachable_states())
        ok_idem &= moore_minimize(m).is_isomorphic(m)
        ok_brute &= brute_force_equal(d, m, max_len=4)
    check("minimized DFAs are equivalent to originals", ok_equiv)
    check("minimized DFAs are never larger", ok_size)
    check("minimizing twice changes nothing", ok_idem)
    check("brute-force word check agrees", ok_brute)


def main():
    print("Example DFA:")
    print(EXAMPLE)
    print("\nMinimized:")
    print(moore_minimize(EXAMPLE))
    print()

    for test in (test_construction, test_acceptance, test_minimization_helpers,
                 test_comparison, test_random):
        test()
        print()

    print(f"{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
