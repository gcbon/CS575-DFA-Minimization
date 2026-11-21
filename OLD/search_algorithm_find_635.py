from enum import Enum
from itertools import product
from typing import Iterator, List, Optional, Tuple

import matplotlib.pyplot as plt

from my_dfa import DFA
import work_functions


class Algorithm(Enum):
    FIND_REACHABLE = "find_reachable_work"
    BRZOZOWSKI = "brzozowski_work"
    MYHILL_NERODE = "myhill_nerode_work"


#ALGORITHM = Algorithm.FIND_REACHABLE
# ALGORITHM = Algorithm.MYHILL_NERODE
ALGORITHM = Algorithm.BRZOZOWSKI



Candidate = Tuple[Tuple[int, ...], int, Tuple[bool, ...]]


def _all_candidates(num_states: int, num_symbols: int) -> Iterator[Candidate]:
    for transitions in product(
        range(num_states), repeat=num_states * num_symbols
    ):
        for start in range(num_states):
            for accepting in product((False, True), repeat=num_states):
                yield transitions, start, accepting


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
    dfa = _to_dfa(candidate, num_states, num_symbols)
    if ALGORITHM == Algorithm.FIND_REACHABLE:
        return work_functions.find_reachable_work(dfa)
    if ALGORITHM == Algorithm.BRZOZOWSKI:
        return work_functions.brzozowski_work(dfa)
    if ALGORITHM == Algorithm.MYHILL_NERODE:
        return work_functions.myhill_nerode_work(dfa)
    raise ValueError(f"Unsupported algorithm: {ALGORITHM}")


def find_best_dfa(
    num_states: int = 5,
    num_symbols: int = 2,
    max_candidates: Optional[int] = None,
    report_progress: bool = False,
) -> Tuple[DFA, int, List[int], List[int]]:
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
    best_found_at = 0
    scores = []
    best_scores = []
    for candidate in _all_candidates(num_states, num_symbols):
        if max_candidates is not None and candidates_checked >= max_candidates:
            break
        score = _score(candidate, num_states, num_symbols)
        candidates_checked += 1
        if best_score is None or score > best_score:
            best_candidate = candidate
            best_score = score
            best_found_at = candidates_checked
        if score==635:
            return (
                candidates_checked,
                scores,
                best_scores,
            )
        scores.append(score)
        best_scores.append(best_score)

    if best_candidate is None or best_score is None:
        raise RuntimeError("the search did not evaluate any candidates")
    if report_progress:
        print("Unique DFA candidates tried:", candidates_checked)
        print("Total tries:", candidates_checked)
        print("Tries to find best work:", best_found_at)
    return -1


def main() -> None:
    attempts, scores, best_scores = find_best_dfa(
        num_states=3,
        num_symbols=3,
        max_candidates=None,
        report_progress=True,
    )

    print("Attempts:", attempts)

    plt.scatter(range(len(best_scores)), best_scores, s=2)
    plt.scatter(range(len(scores)), scores, s=2)
    plt.xlabel("DFAs Checked")
    plt.ylabel("Score")
    plt.title("Score and Max Score over Time")
    plt.show()


if __name__ == "__main__":
    main()
