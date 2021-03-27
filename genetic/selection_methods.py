from OE_project1.genetic.population_v1 import Population
import numpy as np

def selection_of_best(population, proc_of_chosen):
    sorted_chromosomes = sorted(population.get_population(), key=lambda x: x.get_dec_value())
    length = len(sorted_chromosomes)
    number_of_best = int(length * proc_of_chosen/100)
    chosen = [sorted_chromosomes[i] for i in range(number_of_best)]
    return chosen


def tournament_selection(population, number_of_tournaments, size_of_tournament):
    pass

def ranking_selection(population, rank_func, copy_func):
    pass

def roulette_selection(population):
    pass


if __name__ == '__main__':
    pop = Population(10,-4,81,4)
    print(pop)
    print(f"best: ")
    for b in selection_of_best(pop, 35):
        print(b)