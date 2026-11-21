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

plt.scatter(range(len(best_scores_genetic)), best_scores_genetic, s=2, label="Genetic (average of 10 attempts)")
plt.scatter(range(len(best_scores_random)), best_scores_random, s=2, label="Random (average of 10 attempts)")
plt.scatter(range(len(best_scores_search)), best_scores_search, s=2, label="Search")
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Evolution of Maximum Work for Myhill Nerode")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig("images/MN-all-max.png", dpi=300, bbox_inches="tight")
plt.show()


best_scores_genetic = np.load("data/genetic-BR-10.npy")
best_scores_genetic = np.mean(best_scores_genetic, axis=0)

best_scores_random =  np.load("data/random-BR-10.npy")
best_scores_random =  np.mean(best_scores_random, axis=0)

best_scores_search =  np.load("data/search-BR-10.npy")

plt.scatter(range(len(best_scores_genetic)), best_scores_genetic, s=2, label="Genetic (average of 10 attempts)")
plt.scatter(range(len(best_scores_random)), best_scores_random, s=2, label="Random (average of 10 attempts)")
plt.scatter(range(len(best_scores_search)), best_scores_search, s=2, label="Search")
plt.xlabel("DFAs Checked")
plt.ylabel("Score")
plt.title("Evolution of Maximum Work for Brzozowski's Algorithm")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig("images/BR-all-max.png", dpi=300, bbox_inches="tight")
plt.show()