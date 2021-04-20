from OE_project1.genetic.genetic import Genetic
import OE_project1.genetic.Geneticutils as gen_utils
import OE_project1.genetic.selection_methods as sel_met
import OE_project1.genetic.mutation.mutation as m
import OE_project1.genetic.crossover as crossover
import tkinter as tk
import tkinter.ttk as ttk

def initializeForm():
    window = tk.Tk()

    lbl_function = tk.Label(window, text="Function")
    lbl_function.pack()
    function_option = ("Booth", "Easom")
    function = ttk.Combobox(window, values=function_option)
    function.pack()

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

    lbl_elitist = tk.Label(window, text="Elitist strategy  %")
    lbl_elitist.pack()
    elitist_proc = tk.Entry(window)
    elitist_proc.pack()

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
    cross_method = ("Homogeneous", "One point", "Two point", "Three point", "Arithmetic", "Heuristic")
    cross = ttk.Combobox(window, values=cross_method)
    cross.pack()

    lbl_mutation = tk.Label(window, text="Mutation method")
    lbl_mutation.pack()
    mutation_method = ("One point", "Two point", "Boundary", "Uniform")
    mut = ttk.Combobox(window, values=mutation_method)
    mut.pack()

    inversion = tk.IntVar()
    inv = tk.Checkbutton(window, text="Inversion", variable=inversion)
    inv.pack()

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
        best_proc.get(),
        function.get(),
        elitist_proc.get(),
        inversion.get(),
    ))
    submit_button.pack()

    quit_button = tk.Button(window, text='Close', command=window.destroy)
    quit_button.pack()

    window.title('Generic algorithm')
    window.geometry("250x650+10+10")
    window.mainloop()


def submit(epochs, population, begin, end, bits, tournament_chromosome, mut_prob, minimization, selection, cross,
           mutation, best_proc, function, elitist_proc, inversion):
    gen = Genetic(number_of_epochs=int(epochs),
                  size_of_population=int(population),
                  value_range=(int(begin), int(end)),
                  number_of_bits=int(bits),
                  minimalization=True if minimization == 1 else False,
                  selection_method=convertSelectionMethods(selection),
                  tournament_size=int(tournament_chromosome),
                  cross_degree=convertCrossMethods(cross),
                  mutation_type=convertMutationMethods(mutation),
                  target_function=convertFunction(function),
                  best_sel_proc=int(best_proc),
                  probablility_of_mutation=int(mut_prob) / 100,
                  proc_of_ind_for_elit=int(elitist_proc),
                  make_inversion=True if inversion == 1 else False
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
        "Three point": crossover.CrossDegree.three_point,
        "Arithmetic": crossover.CrossDegree.arithmetic,
        "Heuristic": crossover.CrossDegree.heuristic,
    }[method]


def convertMutationMethods(method):
    return {
        "One point": m.MutationType.one_point,
        "Two point": m.MutationType.two_point,
        "Boundary": m.MutationType.boundry,
        "Inversion": m.MutationType.inversion,
        "Uniform": m.MutationType.uniform
    }[method]


def convertFunction(method):
    return {
        "Booth": gen_utils.TargetFunction.booth,
        "Easom": gen_utils.TargetFunction.easom,
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
