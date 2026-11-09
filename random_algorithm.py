import random
from typing import Optional, Tuple

from my_dfa import DFA
import work_functions


Candidate = Tuple[Tuple[int, ...], int, Tuple[bool, ...]]


def _random_candidate(
    num_states: int, num_symbols: int, rng: random.Random
) -> Candidate:
    return (
        tuple(
            rng.randrange(num_states)
            for _ in range(num_states * num_symbols)
        ),
        rng.randrange(num_states),
        tuple(rng.choice((False, True)) for _ in range(num_states)),
    )


def _to_dfa(candidate: Candidate, num_states: int, num_symbols: int) -> DFA:
    transitions, start_state, accepting_flags = candidate
    delta = [
        list(transitions[state * num_symbols:(state + 1) * num_symbols])
        for state in range(num_states)
    ]
    accepting = {
        state for state, is_accepting in enumerate(accepting_flags)
        if is_accepting
    }
    return DFA(delta=delta, start=start_state, accepting=accepting)


def _score(candidate: Candidate, num_states: int, num_symbols: int) -> int:
    return work_functions.find_reachable_work(
        _to_dfa(candidate, num_states, num_symbols)
    )


def find_best_dfa(
    num_states: int = 5,
    num_symbols: int = 2,
    guesses: int = 10000,
    seed: Optional[int] = None,
) -> Tuple[DFA, int]:
    """Return the highest-scoring DFA from independently random guesses."""
    if num_states < 1:
        raise ValueError("num_states must be at least 1")
    if num_symbols < 1:
        raise ValueError("num_symbols must be at least 1")
    if guesses < 1:
        raise ValueError("guesses must be at least 1")

    rng = random.Random(seed)
    best_candidate = None
    best_score = None
    for _ in range(guesses):
        candidate = _random_candidate(num_states, num_symbols, rng)
        score = _score(candidate, num_states, num_symbols)
        if best_score is None or score > best_score:
            best_candidate = candidate
            best_score = score

    if best_candidate is None or best_score is None:
        raise RuntimeError("the random search did not evaluate any candidates")
    return _to_dfa(best_candidate, num_states, num_symbols), best_score


def main() -> None:
    best_dfa, score = find_best_dfa(
        num_states=100,
        num_symbols=2,
        guesses=10000,
        seed=None,
    )
    print("Best work:", score)
    print("Start state:", best_dfa.start)
    print("Accepting states:", sorted(best_dfa.accepting))
    print("Transitions:", best_dfa.delta)


if __name__ == "__main__":
    main()
