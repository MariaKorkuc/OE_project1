from OE_project1.genetic.population import Population
from OE_project1.genetic.Geneticutils import chosen_func, get_best
import numpy as np
from enum import Enum


class SelectionMethod(Enum):
    best = 1
    tournament = 2
    roulette = 3



def selection_of_best(population, proc_of_chosen, minimalization=True):
    # w zaleznosci od tego czy ma byc min czy max, trzeba ustalic ktorych osobnikow bierzemy
    reverse = True if not minimalization else False

    # sortowanie według wartosci funkcji dla danego osobnika
    sorted_individuals = sorted(population, key=lambda x: x.get_func_value(), reverse=reverse)
    length = len(sorted_individuals)

    # obliczenie ile najlepszych wybieramy sposrod populacji na podstawie przekazanego procenta
    number_of_best = int(length * proc_of_chosen/100)
    number_of_best = max((1,number_of_best))
    chosen = [sorted_individuals[i] for i in range(number_of_best)]
    return chosen

def tournament(individuals, size_of_tournament, minimalization):
    if len(individuals) == 1:
        return individuals[0]

    number_of_tournaments = len(individuals) // size_of_tournament

    if len(individuals) % size_of_tournament:
        number_of_tournaments += 1

    tournaments = [[] for _ in range(number_of_tournaments)]

    for t in range(number_of_tournaments):
        for i in range(size_of_tournament):
            if t*size_of_tournament + i < len(individuals):
                tournaments[t].append(individuals[t*size_of_tournament + i])

    best = [get_best(tournaments[t], minimalization) for t in range(number_of_tournaments)]

    return tournament(best, size_of_tournament, minimalization)


def tournament_selection(population, size_of_tournament, minimalization=True):
    shuffled_indexes = np.random.permutation([i for i in range(len(population))])
    shuffled_pop = [population[i] for i in shuffled_indexes]
    return tournament(shuffled_pop, size_of_tournament, minimalization)


def get_distributions(population, minimalization):
    min_func_val = min([ind.get_func_value() for ind in population])
    scale = abs(min_func_val) + 1 if min_func_val < 0 else 0

    if minimalization:
        values = [1/(ind.get_func_value() + scale) for ind in population]
        sum_func = sum(1/v for v in values)
    else:
        values = [(ind.get_func_value() + scale) for ind in population]
        sum_func = sum(values)
    probabilities = [val / sum_func for val in values]
    distributions = [probabilities[0]]

    for i in range(1, len(probabilities)):
        distributions.append(distributions[i-1] + probabilities[i])
    return distributions


def roulette_selection(population, minimalization=True):
    distributions = get_distributions(population, minimalization)
    values = tuple(zip(population, distributions))
    random_prob = np.random.uniform(min(distributions), max(distributions))
    result = values[0][0]
    for ind, d in values:
        if d < random_prob:
            result = ind
        else:
            break
    return result


