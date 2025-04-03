'Calculating Permutation Entropy from a time series'

import itertools
import numpy as np
import pandas as pd
from typing import List


def s_entropy(freq_list: List[float]) -> (float):
    'to calculate shannon entropy'
    freq_list = [element for element in freq_list if element != 0]
    sh_entropy = 0.0
    for freq in freq_list:
        sh_entropy += freq * np.log(freq)
    sh_entropy = -sh_entropy
    return(sh_entropy)

def ordinal_patterns(ts: np.array, embdim: int, embdelay: int) -> (List[float]):
    'to extract the ordinal pattern'
    time_series = ts
    possible_permutations = list(itertools.permutations(range(embdim)))
    lst = list()
    embdimTimesEmbdelay = embdim*embdelay
    for i in range(int(len(time_series) - embdelay * (embdim - 1))):
        a = time_series[i:(embdimTimesEmbdelay+i):embdelay]
        sorted_index_array = list(np.argsort(a))
        lst.append(sorted_index_array)
    lst = np.array(lst)
    element, freq = np.unique(lst, return_counts=True, axis=0)
    freq = list(freq)
    if len(freq) != len(possible_permutations):
        for i in range(len(possible_permutations)-len(freq)):
            freq.append(0)
        return(freq)
    else:
        return(freq)


def p_entropy(op: List[float]) -> (float):
    'to calculate permutation entropy'
    ordinal_pat = op
    max_entropy = np.log(len(ordinal_pat))
    p = np.divide(np.array(ordinal_pat), float(sum(ordinal_pat)))
    return(s_entropy(p)/max_entropy)
