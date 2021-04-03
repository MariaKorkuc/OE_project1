import numpy as np


def chosen_func(Xs):
    return booth_function_temp(Xs)


def booth_function_temp(Xs):
    return np.power(Xs[0] + 2*Xs[1] - 7, 2) + np.power(2*Xs[0] + Xs[1] - 5, 2)


def get_best(arr, minimalization):
    values = [(ind, ind.get_func_value()) for ind in arr]
    val = lambda x: x[1]
    return min(values, key=val)[0] if minimalization else max(values, key=val)[0]