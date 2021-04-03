import random
from OE_project1.genetic.population import Individual, Chromosome
from OE_project1.genetic.selection_methods import SelectionMethod
import OE_project1.genetic.selection_methods as selection



def cross(binary1, binary2, cross_degree, number_of_bits):
    # listy na dany chromosom dla 1 osobnika i 2 osobnika
    new_binary_1 = []
    new_binary_2 = []

    # dla krzyżownania jednorodnego
    if cross_degree == 0:
        for i in range(number_of_bits):
            if i%2:
                new_binary_1.append(binary1[i])
                new_binary_2.append(binary2[i])
            else:
                new_binary_1.append(binary2[i])
                new_binary_2.append(binary1[i])
        return new_binary_1, new_binary_2

    # lista indeksów, gdzie mają być punkty krzyżowania, ich ilość zależna od cross_degree
    cross_points = []

    # uzupełnianie listy cross_points i sortowanie (idziemy z punktami krzyżowania po kolei)
    for _ in range(cross_degree):
        cross_points.append(random.randrange(0, number_of_bits))
    cross_points.sort()

    # na razie lista cross_points bedzie wskazywac na indeks pierwszego punktu krzyżownia
    point_index = 0
    # wartosc mowiaca o tym, czy nastapil punkt krzyzowania i czy nalezy krzyzowac (dla nieparzystych p.k.), czy
    # "odkrzyzowac" (dla parzystych)
    exchange = False

    # idziemy po wszystkich bitach chromosomu
    for i in number_of_bits:
        # patrzymy na punkt krzyżowania - jeśli go przekraczamy, to zmieniamy wartosc exchange,
        if point_index < len(cross_points) and i == cross_points[point_index]:
            exchange = not exchange
            # teraz patrzymy kiedy bedzie nastepny punkt krzyzowania
            point_index += 1
        # jak mamy krzyżować - wymieniamy wartosci, jak nie, to nie
        if exchange:
            new_binary_1.append(binary2[i])
            new_binary_2.append((binary1[i]))
        else:
            new_binary_1.append(binary1[i])
            new_binary_2.append((binary2[i]))

        # if point_index < len(cross_points) and i == cross_points[point_index] and point_index%2:
        #     new_binary_1.append(binary2[i])
        #     new_binary_2.append((binary1[i]))
        #     point_index += 1
        # else:
        #     new_binary_1.append(binary1[i])
        #     new_binary_2.append((binary2[i]))
        #     if point_index < len(cross_points) and i == cross_points[point_index]:
        #         point_index += 1

    # zwracamy wartosc chromosomu dla nowego osobnika 1 i nowego osobnika 2
    return new_binary_1, new_binary_2

# cross_degree = 0 => krzyżowanie jednorodne
def crossover(first_ind, second_ind, number_of_bits, cross_degree=1):
    # ile ma byc chromosomow w osobniku
    number_of_chromosomes_per_ind = len(first_ind)
    value_range = first_ind.get_value_range()

    # sprawdzenie, czy osobniki maja po tyle samo chromosomow
    if len(first_ind) != len(second_ind):
        return None

    # nowe listy chromosomow dla nowego osobnika 1 i nowego osobnika 2
    new_chromosomes_1 = []
    new_chromosomes_2 = []

    # iteracja po wszystkich chromosomach w osobniku, czyli w przypadku f. dwoch zmiennych: 1 osobnik = 2 chromosomy
    for i in range(number_of_chromosomes_per_ind):
        # gettery wartosci binarnych rodzicow
        old_value_1 = first_ind[i].get_binary()
        old_value_2 = second_ind[i].get_binary()

        # generowanie danego chromosomu dla obu dzieci
        new_value_1, new_value_2 = cross(old_value_1, old_value_2, cross_degree, number_of_bits)

        # dodawanie nowych chromosomow do kazdego z dzieci
        new_chromosomes_1.append(Chromosome(number_of_bits, value_range, binary=new_value_1))
        new_chromosomes_2.append(Chromosome(number_of_bits, value_range, binary=new_value_2))

    # zwracanie dwoch nowych osobnikow (dzieci) z krzyzowki rodzicow
    return Individual(value_range, number_of_bits, number_of_chromosomes_per_ind, new_chromosomes_1), \
        Individual(value_range, number_of_bits, number_of_chromosomes_per_ind, new_chromosomes_2)


def create_new_population(population, selection_method, cross_degree, minimalization, **selection_args):
    pop_size = len(population)
    new_individuals = []

    while len(new_individuals) < pop_size:
        if selection_method == SelectionMethod.best:
            best = selection.selection_of_best(population, selection_args['proc_of_chosen'], minimalization)
