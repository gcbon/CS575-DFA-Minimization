import random
import sys

from my_dfa import DFA
import work_functions

import random_algorithm
import search_algorithm
import genetic_algorithm

search_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    max_candidates=1000
)