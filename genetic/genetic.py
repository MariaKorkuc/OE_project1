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
import tkinter as tk
import tkinter.ttk as ttk


class Genetic:
    # TODO: rozna ilosc bitow dla chromosomow
    def __init__(self,
                 number_of_epochs=300,
                 size_of_population=50,
                 value_range=(-10, 10),
                 number_of_bits=15,
                 chromosomes_per_ind=2,
                 target_function=gen_utils.TargetFunction.booth,
                 selection_method=sel_met.SelectionMethod.roulette,
                 minimalization=True,
                 cross_degree=crossover.CrossDegree.one_point,
                 mutation_type=m.MutationType.one_point,
                 probablility_of_mutation=0.5,
                 proc_of_ind_for_elit=5,
                 best_sel_proc=None,
                 tournament_size=None,
                 filename='result',
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
        self.population = self.get_initial_population(size_of_population, value_range[0], value_range[1],
                                                      number_of_bits, chromosomes_per_ind)
        self.mutation = self.get_mutation(probablility_of_mutation)
        self.proc_of_elite = proc_of_ind_for_elit

    def get_initial_population(self, size, range_start, range_stop, number_of_bits,
                               chromosomes_per_individual=2):
        return pop.Population(size, range_start, range_stop, number_of_bits, target_func=self.target_func,
                              chromosomes_per_individual=chromosomes_per_individual)

    def get_mutation(self, probability):
        return m.Mutation(probability)

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
        elitist = sel_met.selection_of_best(self.population, self.proc_of_elite, self.minimalization)
        new_pop, current_best = crossover.create_new_population(self.population, self.selection_method,
                                                                self.cross_degree, self.minimalization,
                                                                self.selection_best_proc, self.tournament_size,
                                                                len(elitist))
        self.mutate(new_pop)
        if len(elitist) > 0:
            new_pop.add_ind(elitist)
        self.population = new_pop

        best_elite_value = elitist[0].get_func_value()
        current_best_value = current_best.get_func_value()
        if self.minimalization:
            current_best = current_best if best_elite_value > current_best_value else elitist[0]
        else:
            current_best = current_best if best_elite_value < current_best_value else elitist[0]
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
        type = 'Min' if self.minimalization else "Max"
        title = '_'.join((type, self.target_func.name))
        plt.title(title)
        plt.savefig(
            f'../Files/{type}_{self.target_func.name}_{self.selection_method.name}_{self.cross_degree.name}_{self.mutation_type.name}.png')

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


def initializeForm():
    window = tk.Tk()

    lbl_begin = tk.Label(window, text="Begin")
    lbl_begin.pack()
    begin = tk.Entry(window)
    begin.pack()

    lbl_end = tk.Label(window, text="End")
    lbl_end.pack()
    end = tk.Entry(window)
    end.pack()

    lbl_epochs = tk.Label(window, text="Epochs amount")
    lbl_epochs.pack()
    epochs = tk.Entry(window)
    epochs.pack()

    lbl_population = tk.Label(window, text="Population amount")
    lbl_population.pack()
    population = tk.Entry(window)
    population.pack()

    lbl_bits = tk.Label(window, text="Number of bits")
    lbl_bits.pack()
    bits = tk.Entry(window)
    bits.pack()

    lbl_cross_prob = tk.Label(window, text="Mutation probability %")
    lbl_cross_prob.pack()
    cross_prob = tk.Entry(window)
    cross_prob.pack()

    lbl_best_proc = tk.Label(window, text="Best selection procent %")
    lbl_best_proc.pack()
    best_proc = tk.Entry(window)
    best_proc.pack()

    lbl_tournament_chrom = tk.Label(window, text="Tournament chromosome amount")
    lbl_tournament_chrom.pack()
    tournament_chrom = tk.Entry(window)
    tournament_chrom.pack()

    minimization = tk.IntVar()
    min = tk.Checkbutton(window, text="Minimization", variable=minimization)
    min.pack()

    lbl_selection = tk.Label(window, text="Selection method")
    lbl_selection.pack()
    selection_method = ("Best", "Tournament", "Roulette")
    sel = ttk.Combobox(window, values=selection_method)
    sel.pack()

    lbl_crossover = tk.Label(window, text="Crossover method")
    lbl_crossover.pack()
    cross_method = ("Homogeneous", "One point", "Two point", "Three point")
    cross = ttk.Combobox(window, values=cross_method)
    cross.pack()

    lbl_mutation = tk.Label(window, text="Mutation method")
    lbl_mutation.pack()
    mutation_method = ("One point", "Two point", "Inversion", "Boundary")
    mut = ttk.Combobox(window, values=mutation_method)
    mut.pack()

    submit_button = tk.Button(window, text='Submit', command=lambda: submit(
        epochs.get(),
        population.get(),
        begin.get(),
        end.get(),
        bits.get(),
        cross_prob.get(),
        tournament_chrom.get(),
        minimization.get(),
        sel.get(),
        cross.get(),
        mut.get(),
        best_proc.get()
    ))
    submit_button.pack()

    quit_button = tk.Button(window, text='Close', command=window.destroy)
    quit_button.pack()

    window.title('Generic algorithm')
    window.geometry("250x550+10+10")
    window.mainloop()


def submit(epochs, population, begin, end, bits, tournament_chromosome, mut_prob, minimization, selection, cross,
           mutation, best_proc):
    gen = Genetic(number_of_epochs=int(epochs),
                  size_of_population=int(population),
                  value_range=(int(begin), int(end)),
                  number_of_bits=int(bits),
                  minimalization=True if minimization == 1 else False,
                  selection_method=convertSelectionMethods(selection),
                  tournament_size=int(tournament_chromosome),
                  cross_degree=convertCrossMethods(cross),
                  mutation_type=convertMutationMethods(mutation),
                  target_function=gen_utils.TargetFunction.booth,
                  best_sel_proc=int(best_proc),
                  probablility_of_mutation=int(mut_prob) / 100
                  )

    gen.run_genetic_algorithm()
    gen.plot_results()
    showResult(gen.get_mean_sd(), gen.gettime())



def convertSelectionMethods(method):
    return {
        "Best": sel_met.SelectionMethod.best,
        "Tournament": sel_met.SelectionMethod.tournament,
        "Roulette": sel_met.SelectionMethod.roulette
    }[method]


def convertCrossMethods(method):
    return {
        "Homogeneous": crossover.CrossDegree.homogenous,
        "One point": crossover.CrossDegree.one_point,
        "Two point": crossover.CrossDegree.two_point,
        "Three point": crossover.CrossDegree.three_point
    }[method]


def convertMutationMethods(method):
    return {
        "One point": m.MutationType.one_point,
        "Two point": m.MutationType.two_point,
        "Boundary": m.MutationType.boundry,
        "Inversion": m.MutationType.inversion
    }[method]


def showResult(mean, timer):
    window = tk.Tk()

    lbl = tk.Label(window, text="Mean | Standard deviation")
    lbl.pack()
    mean_label = tk.Label(window, text=mean)
    mean_label.pack()

    lbl = tk.Label(window, text="Execution time")
    lbl.pack()
    time_label = tk.Label(window, text=timer)
    time_label.pack()

    quit_button = tk.Button(window, text='Close', command=window.destroy)
    quit_button.pack()

    window.title('Results')
    window.geometry("250x200+10+10")
    window.mainloop()


if __name__ == '__main__':
    initializeForm()
    # gen = Genetic(number_of_epochs=800,
    #               size_of_population=150,
    #               value_range=(-15, 15),
    #               number_of_bits=10,
    #               chromosomes_per_ind=2,
    #               target_function=gen_utils.TargetFunction.booth,
    #               selection_method=sel_met.SelectionMethod.tournament,
    #               minimalization=True,
    #               cross_degree=crossover.CrossDegree.three_point,
    #               mutation_type=m.MutationType.one_point,
    #               probablility_of_mutation=0.4,
    #               proc_of_ind_for_elit=5,
    #               best_sel_proc=30,
    #               tournament_size=6,
    #               filename='../Files/results_1.txt')
    # gen.run_genetic_algorithm()
    # print(gen.get_mean_sd())
    # print(gen.gettime())
    # gen.plot_results()
