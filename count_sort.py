import numpy as np


def count_sort(arr: np.array) -> np.array:
    rd = {}
    for ele in arr:
        rd.setdefault(ele, 0)
        rd[ele] += 1

    lt = list(rd.items())
    lt.sort(reverse=True, key=lambda pair: pair[1])

    return np.array(lt)
