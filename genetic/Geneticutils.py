import numpy as np
import math
from enum import Enum


class TargetFunction(Enum):
    booth = 1
    easom = 2

def chosen_func(Xs):
    return easom_function(Xs)


def booth_function(Xs):
    return np.power(Xs[0] + 2*Xs[1] - 7, 2) + np.power(2*Xs[0] + Xs[1] - 5, 2)

def easom_function(Xs):
    x1 = Xs[0]
    x2 = Xs[1]
    return -np.cos(x1) * np.cos(x2) * np.exp(-np.power(x1 - math.pi, 2) - np.power(x2 - math.pi, 2))


def get_best(arr, minimalization):
    values = [(ind, ind.get_func_value()) for ind in arr]
    val = lambda x: x[1]
    return min(values, key=val)[0] if minimalization else max(values, key=val)[0]