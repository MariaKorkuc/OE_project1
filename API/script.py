from genetic.population import Population

range = input("Insert range (e.g. (a,b)): ")
range_start = int(range[1])
range_end = int(range[3])
n = int(input("Size of population: "))
number_of_bits = int(input("Number of bits: "))
epochs = int(input("Number of epochs: "))
selection_method = ''

while selection_method not in ['b','r','t','k']:
    selection_method = input('''Decide on selection method:
        b - selection of best
        r - roulette
        t - tournament selection
        k - ranking
    ''')

if selection_method == 'b':
    proc_chrom_to_hybride = int(input('Insert % of population for hybridization: '))
    proc_best_chosen = int(input('Insert % of best chromosomes_binary to be chosen: '))
elif selection_method == 't':
    number_of_tours = int(input('Number of tournaments: '))
    tour_size = int(input('Size of tournament: '))
elif selection_method == 'k':
    pass



