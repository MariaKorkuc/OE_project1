import random
from OE_project1.genetic.population import Population, Individual, Chromosome
from OE_project1.genetic.selection_methods import SelectionMethod
import OE_project1.genetic.selection_methods as selection
from enum import Enum

class CrossDegree(Enum):
    homogenous = 0
    one_point = 1
    two_point = 2
    three_point = 3


def cross(binary1, binary2, cross_degree, number_of_bits):
    new_binary_1 = []
    new_binary_2 = []

    if cross_degree == CrossDegree.homogenous:
        for i in range(number_of_bits):
            if i%2:
                new_binary_1.append(binary1[i])
                new_binary_2.append(binary2[i])
            else:
                new_binary_1.append(binary2[i])
                new_binary_2.append(binary1[i])
        return new_binary_1, new_binary_2

    cross_points = []

    for _ in range(cross_degree.value):
        cross_points.append(random.randrange(0, number_of_bits))
    cross_points.sort()
    point_index = 0
    exchange = False

    for i in range(number_of_bits):
        if point_index < len(cross_points) and i == cross_points[point_index]:
            exchange = not exchange
            point_index += 1
        if exchange:
            new_binary_1.append(binary2[i])
            new_binary_2.append((binary1[i]))
        else:
            new_binary_1.append(binary1[i])
            new_binary_2.append((binary2[i]))

    return new_binary_1, new_binary_2

def crossover(first_ind, second_ind, number_of_bits, target_func, cross_degree=CrossDegree.one_point):
    number_of_chromosomes_per_ind = len(first_ind)
    value_range = first_ind.get_value_range()

    if len(first_ind) != len(second_ind):
        return None

    new_chromosomes_1 = []
    new_chromosomes_2 = []

    for i in range(number_of_chromosomes_per_ind):
        old_value_1 = first_ind[i].get_binary()
        old_value_2 = second_ind[i].get_binary()

        new_value_1, new_value_2 = cross(old_value_1, old_value_2, cross_degree, number_of_bits)

        new_chromosomes_1.append(Chromosome(number_of_bits, value_range, binary=new_value_1))
        new_chromosomes_2.append(Chromosome(number_of_bits, value_range, binary=new_value_2))

    return Individual(value_range, number_of_bits, number_of_chromosomes_per_ind, target_func, new_chromosomes_1), \
        Individual(value_range, number_of_bits, number_of_chromosomes_per_ind, target_func, new_chromosomes_2)


def create_new_population(population, selection_method, cross_degree, minimalization, selection_best_proc=None,
                          tournament_size=None, elitist_length=0):
    pop_size = len(population) - elitist_length
    target_func = population.get_target_func()
    new_individuals = []
    best_individual = None

    if selection_method == SelectionMethod.best:
        best = selection.selection_of_best(population, selection_best_proc, minimalization)
        best_individual = best[0]
        while len(new_individuals) < pop_size:
            parents = random.sample(best, 2)
            probability_of_crossover = random.random()
            if probability_of_crossover >= 0.5:
                children = \
                    crossover(parents[0], parents[1], population.get_number_of_bits_per_chromosome(), target_func, cross_degree)
                new_individuals.extend(children)
    elif selection_method == SelectionMethod.tournament:
        while len(new_individuals) < pop_size:
            parents = \
                [selection.tournament_selection(population, tournament_size, minimalization)
                    for _ in range(2)]
            best_individual = parents[0]
            probability_of_crossover = random.random()
            if probability_of_crossover >= 0.5:
                children = \
                    crossover(parents[0], parents[1], population.get_number_of_bits_per_chromosome(), target_func, cross_degree)
                new_individuals.extend(children)
    elif selection_method == SelectionMethod.roulette:
        while len(new_individuals) < pop_size:
            parents = [selection.roulette_selection(population, minimalization) for _ in range(2)]
            best_individual = parents[0]
            probability_of_crossover = random.random()
            if probability_of_crossover >= 0.5:
                children = \
                    crossover(parents[0], parents[1], population.get_number_of_bits_per_chromosome(), target_func, cross_degree)
                new_individuals.extend(children)
    return Population(
        pop_size,
        population.get_range()[0],
        population.get_range()[1],
        population.get_number_of_bits_per_chromosome(),
        individuals=new_individuals), \
        best_individual


if __name__ == '__main__':
    pop = Population(size=30, range_start=-5, range_stop=5, number_of_bits=8, seed=None)
    print(pop.get_sorted())
    print('********* N E W *********')
    new_pop = create_new_population(pop, SelectionMethod.best, CrossDegree.one_point, minimalization=True, proc_of_chosen=40)
    print(new_pop.get_sorted())
    print(f'--------------- SUM old: {pop.get_sum()} ----------------')
    print(f'--------------- SUM new: {new_pop.get_sum()} ----------------')
