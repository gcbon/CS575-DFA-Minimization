import random
import sys
import matplotlib.pyplot as plt

from my_dfa import DFA
import work_functions

import random_algorithm
import search_algorithm
import genetic_algorithm


search_algorithm.ALGORITHM = search_algorithm.Algorithm.MYHILL_NERODE

best_dfa, score, scores, best_scores = search_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    max_candidates=1024,
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
plt.savefig("images/search-MN.png", dpi=300, bbox_inches="tight")
plt.show()

random_algorithm.ALGORITHM = random_algorithm.Algorithm.MYHILL_NERODE

best_dfa, score, scores, best_scores = random_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    guesses=1024,
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
plt.savefig("images/random-MN.png", dpi=300, bbox_inches="tight")
plt.show()


genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.MYHILL_NERODE

best_dfa, score, scores, best_scores = genetic_algorithm.find_best_dfa(
    num_states = 10,
    num_symbols = 2,
    population_size=16,
    generations=64,
    mutation_rate=0.05,
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
plt.savefig("images/genetic-MN.png", dpi=300, bbox_inches="tight")
plt.show()


search_algorithm.ALGORITHM = search_algorithm.Algorithm.BRZOZOWSKI

best_dfa, score, scores, best_scores = search_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    max_candidates=1024,
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
plt.savefig("images/search-BR.png", dpi=300, bbox_inches="tight")
plt.show()

random_algorithm.ALGORITHM = random_algorithm.Algorithm.BRZOZOWSKI

best_dfa, score, scores, best_scores = random_algorithm.find_best_dfa(
    num_states=10,
    num_symbols=2,
    guesses=1024,
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
plt.savefig("images/random-BR.png", dpi=300, bbox_inches="tight")
plt.show()


genetic_algorithm.ALGORITHM = genetic_algorithm.Algorithm.BRZOZOWSKI

best_dfa, score, scores, best_scores = genetic_algorithm.find_best_dfa(
    num_states = 10,
    num_symbols = 2,
    population_size=16,
    generations=64,
    mutation_rate=0.05,
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
plt.savefig("images/genetic-BR.png", dpi=300, bbox_inches="tight")
plt.show()

