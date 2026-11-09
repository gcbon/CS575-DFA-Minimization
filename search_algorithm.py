from itertools import product
from typing import Iterator, Optional, Tuple

from my_dfa import DFA
import work_functions


Candidate = Tuple[Tuple[int, ...], int, Tuple[bool, ...]]


def _all_candidates(num_states: int, num_symbols: int) -> Iterator[Candidate]:
    for transitions in product(
        range(num_states), repeat=num_states * num_symbols
    ):
        for start_state in range(num_states):
            for accepting in product((False, True), repeat=num_states):
                yield transitions, start_state, accepting


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
    max_candidates: Optional[int] = None,
) -> Tuple[DFA, int]:
    """Return the best DFA in the enumerated candidate space."""
    if num_states < 1:
        raise ValueError("num_states must be at least 1")
    if num_symbols < 1:
        raise ValueError("num_symbols must be at least 1")
    if max_candidates is not None and max_candidates < 1:
        raise ValueError("max_candidates must be at least 1")

    best_candidate = None
    best_score = None
    candidates_checked = 0
    for candidate in _all_candidates(num_states, num_symbols):
        if max_candidates is not None and candidates_checked >= max_candidates:
            break
        score = _score(candidate, num_states, num_symbols)
        candidates_checked += 1
        if best_score is None or score > best_score:
            best_candidate = candidate
            best_score = score

    if best_candidate is None or best_score is None:
        raise RuntimeError("the search did not evaluate any candidates")
    return _to_dfa(best_candidate, num_states, num_symbols), best_score


def main() -> None:
    best_dfa, score = find_best_dfa(
        num_states=4,
        num_symbols=2,
        max_candidates=None,
    )
    print("Best work:", score)
    print("Start state:", best_dfa.start)
    print("Accepting states:", sorted(best_dfa.accepting))
    print("Transitions:", best_dfa.delta)


if __name__ == "__main__":
    main()
