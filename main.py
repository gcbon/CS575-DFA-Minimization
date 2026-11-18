import random
import sys
import matplotlib.pyplot as plt

from my_dfa import DFA
import work_functions

import random_algorithm
import search_algorithm
import genetic_algorithm


search_algorithm.ALGORITHM = search_algorithm.Algorithm.MYHILL_NERODE

_, score, scores, best_scores = search_algorithm.find_best_dfa(
    num_states=3,
    num_symbols=3,
    max_candidates=157464,
    report_progress=True,
)

print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/search-MN-4.png", dpi=300, bbox_inches="tight")
plt.show()

random_algorithm.ALGORITHM = random_algorithm.Algorithm.MYHILL_NERODE

_, score, scores, best_scores = random_algorithm.find_best_dfa(
    num_states=3,
    num_symbols=3,
    guesses=157464,
    seed=None,
    report_progress=True,
)
print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/random-MN-4.png", dpi=300, bbox_inches="tight")
plt.show()


genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.MYHILL_NERODE

_, score, scores, best_scores = genetic_algorithm.find_best_dfa(
    num_states = 3,
    num_symbols = 3,
    population_size=16,
    generations=int(157464/16),
    mutation_rate=0.05,
    seed=None,
    report_progress=True,
)

print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/genetic-MN-4.png", dpi=300, bbox_inches="tight")
plt.show()


search_algorithm.ALGORITHM = search_algorithm.Algorithm.BRZOZOWSKI

_, score, scores, best_scores = search_algorithm.find_best_dfa(
    num_states=3,
    num_symbols=3,
    max_candidates=157464,
    report_progress=True,
)

print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/search-BR-4.png", dpi=300, bbox_inches="tight")
plt.show()

random_algorithm.ALGORITHM = random_algorithm.Algorithm.BRZOZOWSKI

_, score, scores, best_scores = random_algorithm.find_best_dfa(
    num_states=3,
    num_symbols=3,
    guesses=157464,
    seed=None,
    report_progress=True,
)
print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/random-BR-4.png", dpi=300, bbox_inches="tight")
plt.show()


genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.BRZOZOWSKI

_, score, scores, best_scores = genetic_algorithm.find_best_dfa(
    num_states = 3,
    num_symbols = 3,
    population_size=16,
    generations=int(157464/16),
    mutation_rate=0.05,
    seed=None,
    report_progress=True,
)

print("Best work:", score)

plt.scatter(range(len(best_scores)), best_scores, s=2)
plt.scatter(range(len(scores)), scores, s=2)
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Score and Max Score over Time")
plt.savefig("images/genetic-BR-4.png", dpi=300, bbox_inches="tight")
plt.show()

