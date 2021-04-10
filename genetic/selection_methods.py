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

    # zwrocenie najlepszych osobnikow
    return chosen

# funkcja selekcji turniejowej - REKURENCJA
def tournament(individuals, size_of_tournament, minimalization):
    # jeśli zostal tylko jeden osobnik w liscie - zwracamy zwyciesce
    if len(individuals) == 1:
        return individuals[0]

    # obliczenie liczby turniejow w zaleznosci od aktualnej wielkosci listy osobnikow i wielkosci turnieju
    number_of_tournaments = len(individuals) // size_of_tournament

    # jesli mamy reszte (np. pop=36, size_of_tournament=5) to musimy dodac oddzielny dla niej turniej
    if len(individuals) % size_of_tournament:
        number_of_tournaments += 1

    # lista turniejow w aktualnej rundzie
    tournaments = [[] for _ in range(number_of_tournaments)]

    # podzielenie calej populacji na number_of_tournaments turniejow
    for t in range(number_of_tournaments):
        for i in range(size_of_tournament):
            if t*size_of_tournament + i < len(individuals):
                tournaments[t].append(individuals[t*size_of_tournament + i])

    # wybor najlepszych z kazdej grupy turniejowej - lista osobnikow, ktorzy przechodza do nastepnej rundy
    best = [get_best(tournaments[t], minimalization) for t in range(number_of_tournaments)]

    # rekurencyjnie powtarzamy dla kolejnej rundy
    return tournament(best, size_of_tournament, minimalization)


def tournament_selection(population, size_of_tournament, minimalization=True):
    # permutacje zeby nie wybierac zawsze tych samych grup turniejowych
    shuffled_indexes = np.random.permutation([i for i in range(len(population))])
    shuffled_pop = [population[i] for i in shuffled_indexes]  #now we'll take indexes one_point after another to have random tournaments
    return tournament(shuffled_pop, size_of_tournament, minimalization)
    # number_of_tournaments = shuffled.size//size_of_tournament

    # if shuffled.size%size_of_tournament:
    #     number_of_tournaments += 1
    # tournaments = [[] for _ in range(number_of_tournaments)]
    #
    # for t in range(number_of_tournaments):
    #     for i in range(size_of_tournament):
    #         if t*size_of_tournament + i < shuffled.size:
    #             tournaments[t].append(shuffled[t*size_of_tournament + i])
    #         # else:
    #         #     tournaments[t].append(None)
    # best = [get_best(tournaments[t], minimalization) for t in range(number_of_tournaments)]


# zwraca dystrybuanty do selekcji kolem ruletki
def get_distributions(population, minimalization):
    # skalowanie funkcji - unikanie ujemnych prawdopodobienstw, jesli istnieje ujemne wartosci
    min_func_val = min([ind.get_func_value() for ind in population])
    scale = abs(min_func_val) + 1 if min_func_val < 0 else 0


    # liczenie wartosci dla kazdego odobnika, wzor inny dla mini i maksymalizacji
    if minimalization:
        values = [1/(ind.get_func_value() + scale) for ind in population]
        sum_func = sum(1/v for v in values)
    else:
        values = [(ind.get_func_value() + scale) for ind in population]
        sum_func = sum(values)
    # prawdopodobienstwa dla kazdego osobnika
    probabilities = [val / sum_func for val in values]
    # lista na dystrybuanty - pierwszy musi byc uzupelniony dla obiczenia kolejnych
    distributions = [probabilities[0]]

    # obliczanie dystrybuant dla kazdego osobnika
    for i in range(1, len(probabilities)):
        distributions.append(distributions[i-1] + probabilities[i])
    return distributions


def roulette_selection(population, minimalization=True):
    # lista dystrybuant
    distributions = get_distributions(population, minimalization)
    # spięcie wartosci w tuple: (osobnik, dystrybuanta)
    values = tuple(zip(population, distributions))
    # ruletka
    # random_prob = np.random.rand()
    random_prob = np.random.uniform(min(distributions), max(distributions))
    result = values[0][0]
    for ind, d in values:
        if d < random_prob:
            result = ind
        else:
            break
    return result




if __name__ == '__main__':
    pop = Population(size=20, range_start=-5, range_stop=5, number_of_bits=8, seed = None)
    print(pop.get_sorted())
    print("\n******************best************************")
    # for b in selection_of_best(pop, 35):
    #     print(b)
    # for b in tournament_selection(pop, 3):
    #     print(b)
    print(roulette_selection(pop, minimalization=True))
