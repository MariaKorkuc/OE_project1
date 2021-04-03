import numpy as np
import genetic.Geneticutils as gen
import random


class Chromosome:
    def __init__(self, number_of_bits, value_range, binary=None):
        self.binary = [random.randint(0,1) for _ in range(number_of_bits)] if not binary else binary
        self.binary_string = ''.join(str(b) for b in self.binary)
        self.number_of_bits = number_of_bits
        self.start = value_range[0]
        self.stop = value_range[1]
        self.step = self.count_step()

    def get_binary(self):
        return self.binary

    def get_decimal(self):
        return self.start + int(self.binary_string, 2) * self.step

    def set_binary(self, chromosome):
        self.binary = chromosome

    def count_step(self):
        range_size = self.stop - self.start
        possible_combinations = np.power(2, self.number_of_bits)
        return range_size / (possible_combinations - 1)

    def __str__(self):
        return self.binary_string + ' (' + str(self.get_decimal()) + ')'


class Individual:
    def __init__(self, value_range, number_of_bits, number_of_chromosomes, chromosomes=None):
        self.chromosomes = [Chromosome(number_of_bits, value_range) for _ in range(number_of_chromosomes)] \
            if not chromosomes else chromosomes
        self.func_value = gen.chosen_func(self.get_dec_value())
        self.value_range = value_range

    def get_chromosomes(self):
        return self.chromosomes

    def __len__(self):
        return len(self.chromosomes)

    def __getitem__(self, key):
        return self.chromosomes[key]

    def __setitem__(self, key, value):
        self.chromosomes[key] = value

    def __str__(self):
        return ' | '.join(str(ch) for ch in self.chromosomes) + f' -- val: {self.get_func_value()}'

    def get_dec_value(self):
        return [ch.get_decimal() for ch in self.chromosomes]

    def get_func_value(self):
        return self.func_value

    def get_value_range(self):
        return self.value_range


class Population:
    def __init__(self, size, range_start, range_stop, number_of_bits, chromosomes_per_individual=2, individuals=None, seed=None):
        if seed:
            random.seed(seed)
        self.range = (range_start, range_stop)
        self.size = size
        self.chromosomes_per_indiv = chromosomes_per_individual
        self.number_of_bits = number_of_bits
        self.individuals = self.set_individuals() if not individuals else individuals

    def set_individuals(self):
        return [Individual(self.range, self.number_of_bits, self.chromosomes_per_indiv) for _ in range(self.size)]

    def __len__(self):
        return self.size

    def __str__(self):
        return '\n'.join([str(ind) for ind in self.individuals])

    def __getitem__(self, key):
        return self.individuals[key]

    def __setitem__(self, key, value):
        self.individuals[key] = value

    def get_sorted(self, reverse=False):
        srt = sorted(self.individuals, key=lambda x: x.get_func_value(), reverse=reverse)
        return '\n'.join([str(ind) for ind in srt])

    def get_range(self):
        return self.range

    def get_number_of_bits_per_chromosome(self):
        return self.number_of_bits

    def get_size_of_individual(self):
        return self.chromosomes_per_indiv