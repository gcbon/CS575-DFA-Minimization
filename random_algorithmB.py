import random
from enum import Enum
from typing import Optional, Tuple

from my_dfa import DFA
import work_functions

import matplotlib.pyplot as plt


class Algorithm(Enum):
    FIND_REACHABLE = "find_reachable_work"
    BRZOZOWSKI = "brzozowski_work"
    MYHILL_NERODE = "myhill_nerode_work"


ALGORITHM = Algorithm.FIND_REACHABLE

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
    guesses: int = 10000,
    seed: Optional[int] = None,
    report_progress: bool = False,
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
    best_found_at = 0
    seen_candidates = set()
    scores = []
    best_scores = []
    
    for tries in range(1, guesses + 1):
        candidate = _random_candidate(num_states, num_symbols, rng)
        seen_candidates.add(candidate)
        score = _score(candidate, num_states, num_symbols)
        scores.append(score)
        best_scores.append(best_score)
        if best_score is None or score > best_score:
            best_candidate = candidate
            best_score = score
            best_found_at = tries

    if best_candidate is None or best_score is None:
        raise RuntimeError("the random search did not evaluate any candidates")
    if report_progress:
        print("Unique DFA candidates tried:", len(seen_candidates))
        print("Total tries:", guesses)
        print("Tries to find best work:", best_found_at)
    return _to_dfa(best_candidate, num_states, num_symbols), best_score, scores, best_scores


def main() -> None:
    best_dfa, score, scores, best_scores = find_best_dfa(
        num_states=10,
        num_symbols=2,
        guesses=50,
        seed=None,
        report_progress=True,
    )
    print("Best work:", score)
    print("Start state:", best_dfa.start)
    print("Accepting states:", sorted(best_dfa.accepting))
    print("Transitions:", best_dfa.delta)

    plt.scatter(range(len(best_scores)), best_scores, s=2)
    plt.scatter(range(len(scores)), scores, s=2)
    plt.xlabel("DFAs Checked")
    plt.ylabel("Score")
    plt.title("Score and Max Score over Time")
    plt.show()


if __name__ == "__main__":
    main()
