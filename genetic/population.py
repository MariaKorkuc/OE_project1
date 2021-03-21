import numpy as np
import random
import struct
import bitstring

class Chromosome:
    def __init__(self, value, range, number_of_bits):
        self.dec_value = value
        self.range = range
        self.number_of_bits = number_of_bits
        self.bin_value = self.get_bin_value()

    def get_dec_value(self):
        return self.dec_value

    def get_bin_value(self):
        # packed = struct.pack('!f', self.dec_value)
        # binaries = [bin(i) for i in packed]
        # stripped_binaries = [s.replace('0b', '') for s in binaries]
        # padded = [s.rjust(self.number_of_bits, '0') for s in stripped_binaries]
        # return ''.join(padded)
        f1 = bitstring.BitArray(float=self.dec_value, length=32)
        return f1.bin

    def __str__(self):
        return str(f'{self.dec_value} ({self.bin_value})')




class Population:
    def __init__(self, number_of_chromosomes, range_start, range_end, number_of_bits, unique=False, seed=None):
        self.chromosomes = []
        self.range = (range_start, range_end)
        self.n = number_of_chromosomes
        self.number_of_bits = number_of_bits
        self.unique = unique
        # if unique:
        #     try:
        #         self.possible_number()
        #     except Exception as e:
        #         print(e)
        #         exit(-1)
        self.prepare_random_population_dec(seed)

    def prepare_random_population_dec(self, seed=None):
        if seed:
            random.seed(seed)
        for i in range(self.n):
            val = random.uniform(self.range[0], self.range[1])
            # self.chromosomes[0][i] = Chromosome(val, self.range, self.accuracy)
            self.chromosomes.append(Chromosome(val, self.range, self.number_of_bits))

    # def prepare_random_population(self, seed=None):
    #     if seed:
    #         random.seed(seed)
    #     for i in range(self.n):
    #         self.chromosomes_binary.append(self.random_chromosome())

    # def random_chromosome(self):
    #     chrom = ''
    #     if self.unique:
    #         while not chrom or chrom in self.chromosomes_binary:
    #             chr_l = [random.choice(('0', '1')) for _ in range(self.chromosome_size)]
    #             chrom = ''
    #             chrom = chrom.join(chr_l)
    #     else:
    #         chr_l = [random.choice(('0', '1')) for _ in range(self.chromosome_size)]
    #         chrom = chrom.join(chr_l)
    #     return chrom

    def get_population(self):
        return self.chromosomes

    def __str__(self):
        s = ''
        for c in self.chromosomes:
            s += str(c) + '\n'
        return s

    # TODO
    # def possible_number(self):
    # #     possible = 2**self.chromosome_size
    # #     if self.n > possible:
    # #         raise Exception('Size of population is too big for the possible chromosome combinations')
    # maxim = sum([])


if __name__ == '__main__':
    pop = Population(5, 1, 6, 4)
    print(pop.get_population())

