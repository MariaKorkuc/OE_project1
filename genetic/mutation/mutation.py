from random import random, randint
from genetic.population import Chromosome

def flip_bit(bit):
    return 1 if bit == 0 else 0

class Mutation:
    probability = 0
    is_mutate = False

    def __init__(self, probability):
        self.validate_probability(probability)
        self.probability = probability
        self.is_mutate = False

    def validate_probability(self, probability):
        if probability < 0 or probability > 1:
            print('Probability has wrong value')

    def get_probability(self):
        return self.probability

    def set_probability(self, probability):
        self.validate_probability(probability)
        self.probability = probability

    def mutate_boundary(self, chromosome):
        if self.is_mutate:
            return
        else:
            self.is_mutate = self.probability > random()
        chrom = chromosome.get_binary()
        if randint(0, 1) == 0:
            chrom[0] = flip_bit(chrom[0])
        else:
            chrom[-1] = flip_bit(chrom[-1])
        chromosome.set_binary(chrom)
        print(chromosome)

    def one_point(self, chromosome):
        if self.is_mutate:
            return
        else:
            self.is_mutate = self.probability > random()
        chrom = chromosome.get_binary()
        index = randint(0, len(chrom))
        chrom[index] = flip_bit(chrom[index])
        chromosome.set_binary(chrom)
        print(chromosome)

    def two_point(self, chromosome):
        if self.is_mutate:
            return
        else:
            self.is_mutate = self.probability > random()
        chrom = chromosome.get_binary()
        index1 = randint(0, len(chrom))
        if len(chrom) < 2:
            chrom[index1] = flip_bit(chrom[index1])
            return
        index2 = 0
        while True:
            index2 = randint(0, len(chrom))
            if index1 == index2:
                break
        chrom[index1] = flip_bit(chrom[index1])
        chrom[index2] = flip_bit(chrom[index2])
        chromosome.set_binary(chrom)
        print(chromosome)


if __name__ == '__main__':
    mutation = Mutation(0)
    number_of_bits = 8
    value_range = [1, 5]
    chromosome = Chromosome(number_of_bits, value_range)
    print(chromosome)
    mutation.mutate_boundary(chromosome)
    mutation.one_point(chromosome)
    mutation.two_point(chromosome)
    print(chromosome)
