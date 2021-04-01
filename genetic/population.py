import numpy as np
import OE_project1.genetic.Geneticutils as gen
import random


class Chromosome:
    def __init__(self, number_of_bits, value_range):
        self.binary = [random.randint(0,1) for _ in range(number_of_bits)]
        self.binary_string = ''.join(str(b) for b in self.binary)
        self.number_of_bits = number_of_bits
        self.start = value_range[0]
        self.stop = value_range[1]
        self.step = self.count_step()

    def get_binary(self):
        return self.binary

    def get_decimal(self):
        return self.start + int(self.binary_string, 2)*self.step

    def count_step(self):
        range_size = self.stop - self.start
        possible_combinations = np.power(2, self.number_of_bits)
        return range_size/(possible_combinations - 1)

    def __str__(self):
        return self.binary_string + ' (' + str(self.get_decimal()) + ')'


class Individual:
    def __init__(self, value_range, number_of_bits, number_of_chromosomes):
        self.chromosomes = [Chromosome(number_of_bits, value_range) for _ in range(number_of_chromosomes)]
        self.func_value = gen.chosen_func(self.get_dec_value())

    def get_chromosomes(self):
        return self.chromosomes

    def __getitem__(self, key):
        return self.chromosomes[key]

    def __setitem__(self, key, value):
        self.chromosomes[key] = value

    def __str__(self):
        return ' | '.join(str(ch) for ch in self.chromosomes)

    def get_dec_value(self):
        return [ch.get_decimal() for ch in self.chromosomes]

    def get_func_value(self):
        return self.func_value

class Population:
    def __init__(self, size, range_start, range_stop, number_of_bits, chromosomes_per_individual=2, seed = None):
        if seed:
            random.seed(seed)
        self.range = (range_start, range_stop)
        self.size = size
        self.chromosomes_per_indiv = chromosomes_per_individual
        self.number_of_bits = number_of_bits
        self.individuals = self.get_individuals()

    def get_individuals(self):
        return [Individual(self.range, self.number_of_bits, self.chromosomes_per_indiv) for _ in range(self.size)]

    def __len__(self):
        return self.size

    def __str__(self):
        return '\n'.join([str(ind) for ind in self.individuals])

    def __getitem__(self, key):
        return self.individuals[key]

    def __setitem__(self, key, value):
        self.individuals[key] = value

