from genetic.population import Population
from genetic.Geneticutils import chosen_func, get_best
import numpy as np

# TODO: czy nie dorzucić gdzies listy z wartosciami dla kazdego osobnika?

def selection_of_best(population, proc_of_chosen, minimalization=True):
    reverse = True if not minimalization else False
    sorted_individuals = sorted(population.get_individuals(), key=lambda x: chosen_func(x.get_dec_value()), reverse=reverse)
    length = len(sorted_individuals)
    number_of_best = int(length * proc_of_chosen/100)
    chosen = [sorted_individuals[i] for i in range(number_of_best)]
    return chosen


def tournament_selection(population, size_of_tournament, minimalization=True):
    shuffled = np.random.permutation(population.get_individuals()) #now we'll take indexes one after another to have random tournaments
    number_of_tournameents = shuffled.size//size_of_tournament

    if shuffled.size%size_of_tournament:
        number_of_tournameents += 1
    tournaments = [[] for _ in range(number_of_tournameents)]

    for t in range(number_of_tournameents):
        for i in range(size_of_tournament):
            if t*size_of_tournament + i < shuffled.size:
                tournaments[t].append(shuffled[t*size_of_tournament + i])
            # else:
            #     tournaments[t].append(None)
    best = [get_best(tournaments[t], minimalization) for t in range(number_of_tournameents)]
    return best


def get_distributions(population, minimalization):
    if minimalization:
        values = [1/chosen_func(chrom.get_dec_value()) for chrom in population]
        sum_func = sum(1/v for v in values)
    else:
        values = [chosen_func(chrom.get_dec_value()) for chrom in population]
        sum_func = sum(values)
    # probabilities = dict((population[i], values[i] / sum_func) for i in range(len(population)))
    probabilities = [val / sum_func for val in values]
    distributions = [probabilities[0]]
    for i in range(1,len(probabilities)):
        distributions[i] = distributions[i-1] + probabilities[i]
    return distributions


def roulette_selection(population, minimalization=True):
    distributions = get_distributions(population, minimalization)




if __name__ == '__main__':
    pop = Population(size=20, range_start=-5, range_stop=5, number_of_bits=8, seed = None)
    print(pop)
    print("\n******************best************************")
    for b in selection_of_best(pop, 35):
        print(b)
    # for b in tournament_selection(pop, 3):
    #     print(b)
    # roulette_selection(pop)