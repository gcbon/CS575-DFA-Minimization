import random
import sys
import matplotlib.pyplot as plt
import numpy as np

from my_dfa import DFA
import work_functions

import random_algorithm
import search_algorithm
import genetic_algorithm


search_algorithm.ALGORITHM = search_algorithm.Algorithm.MYHILL_NERODE

best_scores_search = search_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    max_candidates=1024,
    report_progress=False,
)[3]
print("search done")
np.save("data/search-MN-10.npy", best_scores_search)

random_algorithm.ALGORITHM = random_algorithm.Algorithm.MYHILL_NERODE

best_scores_random = [random_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    guesses=1024,
    seed=None,
    report_progress=False,
)[3] for _ in range(10)]
print("random done")
np.save("data/random-MN-10.npy", best_scores_random)

genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.MYHILL_NERODE

best_scores_genetic = [genetic_algorithm.find_best_dfa(
    num_states = 10,
    num_symbols = 2,
    population_size=16,
    generations=64,
    mutation_rate=0.05,
    seed=None,
    report_progress=False,
)[3] for _ in range(10)]
print("genetic done")
np.save("data/genetic-MN-10.npy", best_scores_genetic)


search_algorithm.ALGORITHM = search_algorithm.Algorithm.BRZOZOWSKI

best_scores_search = search_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    max_candidates=1024,
    report_progress=False,
)[3]
print("search done")
np.save("data/search-BR-10.npy", best_scores_search)

random_algorithm.ALGORITHM = random_algorithm.Algorithm.BRZOZOWSKI

best_scores_random = [random_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    guesses=1024,
    seed=None,
    report_progress=False,
)[3] for _ in range(10)]
print("random done")
np.save("data/random-BR-10.npy", best_scores_random)

genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.BRZOZOWSKI

best_scores_genetic = [genetic_algorithm.find_best_dfa(
    num_states = 10,
    num_symbols = 2,
    population_size=16,
    generations=64,
    mutation_rate=0.05,
    seed=None,
    report_progress=False,
)[3] for _ in range(10)]
print("genetic done")
np.save("data/genetic-BR-10.npy", best_scores_genetic)