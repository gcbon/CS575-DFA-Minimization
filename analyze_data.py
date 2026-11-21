import random
import sys
import matplotlib.pyplot as plt
import numpy as np

from my_dfa import DFA
import work_functions

import random_algorithm
import search_algorithm
import genetic_algorithm


best_scores_genetic = np.load("data/genetic-MN-10.npy")
best_scores_genetic = np.mean(best_scores_genetic, axis=0)

best_scores_random =  np.load("data/random-MN-10.npy")
best_scores_random =  np.mean(best_scores_random, axis=0)

best_scores_search =  np.load("data/search-MN-10.npy")

# compare important metrics
print("Myhill Nerode")
final_best_genetic = best_scores_genetic[-1]
final_best_random = best_scores_random[-1]
final_best_search = best_scores_search[-1]
print("best scores:")
print("genetic: ",  final_best_genetic)
print("random: ",  final_best_random)
print("search: ",  final_best_search)

print("areas under the curve:")
print("genetic: ",  best_scores_genetic.sum())
print("random: ",  best_scores_random.sum())
print("search: ",  best_scores_search.sum())



best_scores_genetic = np.load("data/genetic-BR-10.npy")
best_scores_genetic = np.mean(best_scores_genetic, axis=0)

best_scores_random =  np.load("data/random-BR-10.npy")
best_scores_random =  np.mean(best_scores_random, axis=0)

best_scores_search =  np.load("data/search-BR-10.npy")

# compare important metrics
print("Brzozowski")
final_best_genetic = best_scores_genetic[-1]
final_best_random = best_scores_random[-1]
final_best_search = best_scores_search[-1]
print("best scores:")
print("genetic: ",  final_best_genetic)
print("random: ",  final_best_random)
print("search: ",  final_best_search)

print("areas under the curve:")
print("genetic: ",  best_scores_genetic.sum())
print("random: ",  best_scores_random.sum())
print("search: ",  best_scores_search.sum())