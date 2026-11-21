# Files included

## Core
* my_dfa.py is the DFA class used for the project
* work_functions.py implements the functions to determine work used by each minimization algorithm
* genetic_algorithm.py, random_algorithm.py, and search_algorithm.py implement the maximization techniques

## Evaluation
* analyze_data.py prints the relevant statistics for the collected data
* create_data.py runs each technique on each algorithm 10 times with a 10x2 DFA. It saves the results to the data folder
* graph_data.py graphs the collected data

## misc
* demo.py is the script used for the demo. It generates graphs of sample runs on a 10x2 DFA
* graph_3x3_case went unused in the final project, but it graphs a case small enough for the search algorithm to find the global maximum. It also proves that the functions work outside of the illustrative example.