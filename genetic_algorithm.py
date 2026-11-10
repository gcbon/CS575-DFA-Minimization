import random
from typing import List, Optional, Tuple

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
    delta = [
        list(candidate[0][state * num_symbols:(state + 1) * num_symbols])
        for state in range(num_states)
    ]
    accepting = {
        state for state, is_accepting in enumerate(candidate[2])
        if is_accepting
    }
    return DFA(
        delta=delta,
        start=candidate[1],
        accepting=accepting,
    )


def _score(
    candidate: Candidate, num_states: int, num_symbols: int
) -> int:
    dfa = _to_dfa(candidate, num_states, num_symbols)
    return work_functions.find_reachable_work(dfa)


def _select_parent(
    scored_population: List[Tuple[Candidate, int]], rng: random.Random
) -> Candidate:
    contestants = rng.sample(scored_population, min(3, len(scored_population)))
    return max(contestants, key=lambda entry: entry[1])[0]


def _make_child(
    first: Candidate,
    second: Candidate,
    num_states: int,
    mutation_rate: float,
    rng: random.Random,
) -> Candidate:
    transitions = [
        rng.choice((first_value, second_value))
        for first_value, second_value in zip(
            first[0], second[0]
        )
    ]
    start_state = rng.choice((first[1], second[1]))
    accepting = [
        rng.choice((first_value, second_value))
        for first_value, second_value in zip(first[2], second[2])
    ]

    for index in range(len(transitions)):
        if rng.random() < mutation_rate:
            transitions[index] = rng.randrange(num_states)

    if rng.random() < mutation_rate:
        start_state = rng.randrange(num_states)

    for index in range(len(accepting)):
        if rng.random() < mutation_rate:
            accepting[index] = not accepting[index]

    return tuple(transitions), start_state, tuple(accepting)


def find_best_dfa(
    num_states: int = 5,
    num_symbols: int = 2,
    population_size: int = 100,
    generations: int = 200,
    mutation_rate: float = 0.05,
    seed: Optional[int] = None,
    report_progress: bool = False,
) -> Tuple[DFA, int]:
    """Return the highest-scoring DFA found by the genetic search."""
    if num_states < 1:
        raise ValueError("num_states must be at least 1")
    if num_symbols < 1:
        raise ValueError("num_symbols must be at least 1")
    if population_size < 2:
        raise ValueError("population_size must be at least 2")
    if generations < 0:
        raise ValueError("generations must not be negative")
    if not 0.0 <= mutation_rate <= 1.0:
        raise ValueError("mutation_rate must be between 0 and 1")

    rng = random.Random(seed)
    population = [
        _random_candidate(num_states, num_symbols, rng)
        for _ in range(population_size)
    ]
    best_candidate = population[0]
    best_score: Optional[int] = None
    best_found_at = 0
    tries = 0
    seen_candidates = set()

    for generation in range(generations + 1):
        scored_population = []
        for candidate in population:
            score = _score(candidate, num_states, num_symbols)
            tries += 1
            seen_candidates.add(candidate)
            scored_population.append((candidate, score))
            if best_score is None or score > best_score:
                best_candidate, best_score = candidate, score
                best_found_at = tries

        generation_best = max(scored_population, key=lambda entry: entry[1])

        if generation == generations:
            break

        next_population = [generation_best[0]]
        while len(next_population) < population_size:
            first = _select_parent(scored_population, rng)
            second = _select_parent(scored_population, rng)
            next_population.append(
                _make_child(first, second, num_states, mutation_rate, rng)
            )
        population = next_population

    if best_score is None:
        raise RuntimeError("the genetic search did not evaluate any candidates")
    if report_progress:
        print("Unique DFA candidates tried:", len(seen_candidates))
        print("Total tries:", tries)
        print("Tries to find best work:", best_found_at)
    return _to_dfa(best_candidate, num_states, num_symbols), best_score


def main() -> None:
    best_dfa, score = find_best_dfa(
        num_states=100,
        num_symbols=2,
        population_size=100,
        generations=200,
        mutation_rate=0.05,
        seed=None,
        report_progress=True,
    )
    print("Best work:", score)
    print("Start state:", best_dfa.start)
    print("Accepting states:", sorted(best_dfa.accepting))
    print("Transitions:", best_dfa.delta)


if __name__ == "__main__":
    main()
