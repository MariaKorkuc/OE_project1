import OE_project1.genetic.population as pop
import OE_project1.genetic.Geneticutils as gen_utils
import OE_project1.genetic.selection_methods as sel_met
import OE_project1.genetic.mutation.mutation as m
import OE_project1.genetic.crossover as crossover
import time
import sys
import numpy as np
import random
import matplotlib.pyplot as plt


class Genetic:
    # TODO: rozna ilosc bitow dla chromosomow
    def __init__(self,
                 number_of_epochs=300,
                 size_of_population=50,
                 value_range=(-10,10),
                 number_of_bits=15,
                 chromosomes_per_ind=2,
                 target_function=gen_utils.TargetFunction.booth,
                 selection_method=sel_met.SelectionMethod.roulette,
                 minimalization=True,
                 cross_degree=crossover.CrossDegree.one_point,
                 mutation_type=m.MutationType.one_point,
                 probablility_of_mutation=0.5,
                 proc_of_ind_for_elit=50,
                 best_sel_proc=None,
                 tournament_size=None,
                 filename=None,
                 seed=None):
        if seed:
            random.seed(seed)
        self.start_time = 0
        self.end_time = 0
        self.best_individuals = []
        self.to_file = False if not filename else True
        self.filename = filename
        self.number_of_epochs = number_of_epochs
        self.cross_degree = cross_degree
        self.minimalization = minimalization
        self.selection_best_proc = best_sel_proc
        self.tournament_size = tournament_size
        self.target_func = target_function
        self.selection_method = selection_method
        self.mutation_type = mutation_type
        self.population = self.get_initial_population(size_of_population, value_range[0], value_range[1], number_of_bits, chromosomes_per_ind)
        self.mutation = self.get_mutation(probablility_of_mutation)


    def get_initial_population(self, size, range_start, range_stop, number_of_bits,
                               chromosomes_per_individual=2):
        return pop.Population(size, range_start, range_stop, number_of_bits, target_func=self.target_func,
                              chromosomes_per_individual=chromosomes_per_individual)

    def get_mutation(self, probability):
        return m.Mutation(probability)
        # if mutation_type == m.MutationType.one_point:
        #     return mutation.one_point
        # if mutation_type == m.MutationType.two_point:
        #     return mutation.two_point
        # if mutation_type == m.MutationType.inversion:
        #     return mutation.inversion
        # if mutation_type == m.MutationType.boundry:
        #     return mutation.mutate_boundary

    def mutate(self, new_pop):
        if self.mutation_type == m.MutationType.boundry:
            for ind in new_pop:
                self.mutation.mutate_boundary(ind[0])
                self.mutation.mutate_boundary(ind[1])
        if self.mutation_type == m.MutationType.one_point:
            for ind in new_pop:
                self.mutation.one_point(ind[0])
                self.mutation.one_point(ind[1])
        if self.mutation_type == m.MutationType.two_point:
            for ind in new_pop:
                self.mutation.two_point(ind[0])
                self.mutation.two_point(ind[1])
        if self.mutation_type == m.MutationType.inversion:
            for ind in new_pop:
                self.mutation.inversion(ind[0])
                self.mutation.inversion(ind[1])

    def epoch(self):
        new_pop, current_best = crossover.create_new_population(self.population, self.selection_method,
                                                                self.cross_degree, self.minimalization,
                                                                self.selection_best_proc, self.tournament_size)
        self.mutate(new_pop)
        self.population = new_pop
        return current_best

    def gettime(self):
        return self.end_time - self.start_time

    def plot_results(self):
        unzipped = list(zip(*self.best_individuals))
        epochs = unzipped[0]
        best = unzipped[1]
        plt.plot(epochs, [x.get_func_value() for x in best])
        plt.xlabel('EPOCH')
        plt.ylabel('VALUE FOR BEST INDIVIDUAL')
        plt.savefig('../Files/function_plot.png')

    def get_mean_sd(self):
        values = np.array([x[1].get_func_value() for x in self.best_individuals])
        m = np.mean(values)
        sd = np.std(values)
        return m, sd

    def genetic_algorithm(self):
        # TODO: dodac dodatkowy warunek stopu (niezmienna wartosc najlepszego)
        last_best = 0
        count_identical_best = 0
        self.start_time = time.time()

        for epoch in range(self.number_of_epochs):
            best_individual = self.epoch()
            if best_individual.get_func_value() == last_best:
                count_identical_best += 1
            else:
                count_identical_best = 0
                last_best = best_individual.get_func_value()
            if count_identical_best == 20:
                break
            self.best_individuals.append((epoch, best_individual))

        self.end_time = time.time()

        for ind in self.best_individuals:
            print(f'epoch: {ind[0]}, best: {ind[1]}')

    def run_genetic_algorithm(self):
        if (self.to_file):
            original_stdout = sys.stdout
            with open(self.filename, 'w') as f:
                sys.stdout = f
                self.genetic_algorithm()
                sys.stdout = original_stdout
        else:
            self.genetic_algorithm()

if __name__ == '__main__':
    gen = Genetic(minimalization=True, selection_method=sel_met.SelectionMethod.best, best_sel_proc=20)
    gen.run_genetic_algorithm()
    print(gen.get_mean_sd())
    print(gen.gettime())
    gen.plot_results()