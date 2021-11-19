import numpy as np


def gini(x):
    unique, counts = np.unique(x, return_counts=True)
    dict_counts = dict(zip(unique, counts))
    p_list = [dict_counts[i] /
              len(x) if i in dict_counts else 0 for i in range(unique.max() + 1)]
    return sum([p * (1-p) for p in p_list])
