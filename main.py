"""Verify that the DFA class in dfa.py behaves correctly.

Run with:  python main.py
Exits with status 1 if any check fails.
"""

import random
import sys

from my_dfa import DFA

EXAMPLE = DFA(
    num_states=2,
    num_symbols=2,
    delta=[[0,1],
           [1,1]],
    start=0,
    accepting=set([0]),
    )

print(EXAMPLE.stats_str())