import random
import copy
import matplotlib.pyplot as plt 

class GeneticAlgorithm:
    def __init__(self, data, **kargs):
        self.data = data
        self.POPULATION_SIZE           = kargs.get("population_size", 50)
        self.MAX_WEIGHT                = kargs.get("max_weight", 12210)
        self.MAX_VOLUME                = kargs.get("max_volume", 12)
        self.MAX_GENERATIONS           = kargs.get("max_generations", 50)
        self.NUMBER_OF_ELITES          = kargs.get("elites", 5)
        self.TOURNAMENT_SELECTION_SIZE = 5
        self.CROSSING_RATE             = 0.8
        self.MUTATION_RATE             = 0.2
        self.population                = self._genPopulation()
        self.evolutionGraph            = []
    
    def fittest(self):
        return self.population[0]

    def printFittest(self):
        fittestOne = self.fittest()
        def print_x_in_row(row_length, x_position):
            print('')
            for _ in range(row_length):
                print('------', end='')
            print('\n|', end='')
            for i in range(row_length):
                if i == x_position:
                    print('  {}  |'.format('X'), end='')
                else:
                    print('     |', end='')
        def print_board_bottom(row_length):
            print('\n', end='')
            for _ in range(row_length):
                print('------', end='')
        num_of_rows = len(fittestOne)
        row_length = num_of_rows    #rows == columns in a chessboard
        for row in range(num_of_rows):
            print_x_in_row(row_length, fittestOne[row])

        print_board_bottom(row_length)
        print('\n')

    def printEvolutionGraph(self):
        _, ax = plt.subplots(figsize=(10, 6))
        xAxis = [iteration for (iteration, _) in self.evolutionGraph]
        yAxis = [self._fitness(chromosome) for (_, chromosome) in self.evolutionGraph]
        
        ax.scatter(x = xAxis, y = yAxis, alpha=0.5)
        
        plt.xlabel("Iteration")
        plt.ylabel("Number of collisions")
        ax.set_yticks(yAxis, minor=True)
        plt.grid(linestyle='--', alpha=0.5)
        plt.plot(xAxis, yAxis)
        plt.show()

    def _genChromosome(self):
        chromosome = self.data[:]
        random.shuffle(chromosome)
        return chromosome

    def _genPopulation(self):
        population = [self._genChromosome() for _ in range(self.POPULATION_SIZE)]
        population.sort(key=lambda x: self._fitness(x), reverse=False)

        return population
    
    def _fitness(self, chromosome):
        collisions = 0
        for item in chromosome:
            item_index = chromosome.index(item)
            for elem in chromosome:
                elem_index = chromosome.index(elem)
                if item_index != elem_index:
                    if item - (elem_index - item_index) == elem \
                        or (elem_index - item_index) + item == elem:
                        collisions += 1
        return collisions
    
    def select_tournament(self, population):
        tournament_pop = []
        i = 0
        while i < self.TOURNAMENT_SELECTION_SIZE :
            tournament_pop.append(population[random.randrange(0,self.POPULATION_SIZE)])
            i += 1
        tournament_pop.sort(key=lambda x: self._fitness(x), reverse=False)
        
        # lists are mutable objects, we use [:] to return a copy
        return tournament_pop[0][:]

    def crossover_chromosomes(self, parent_1, parent_2):
        if random.random() < self.CROSSING_RATE: 
            crossover_index = random.randrange(1, len(parent_1))
            child_1a = parent_1[:crossover_index]
            child_1b = [i for i in parent_2 if i not in child_1a]
            child_1 = child_1a + child_1b

            child_2a = parent_2[crossover_index:]
            child_2b = [i for i in parent_1 if i not in child_2a]
            child_2 = child_2a + child_2b

            return child_1, child_2
        else:
            return parent_1, parent_2

    def mutate_chromosome(self, chromosome):
        if random.random() < self.MUTATION_RATE:
            print("\nMaking a mutation")
            print("From: ",chromosome)

            mutate_index1 = random.randrange(len(chromosome))
            mutate_index2 = random.randrange(len(chromosome))
            chromosome[mutate_index1], chromosome[mutate_index2] = chromosome[mutate_index2], chromosome[mutate_index1]
        
        return chromosome
            
    def run(self):
        i = 0
        reached_max_fitness = False
        while not reached_max_fitness and i < self.MAX_GENERATIONS :
            # No collisions found
            if self._fitness(self.population[0]) == 0:
                reached_max_fitness = True

            # lists are mutable objects, we use [:] to return a copy
            self.evolutionGraph.append((i, self.population[0][:]))
            
            i += 1
            new_population = []
            '''Keep The Fittest Chromosomes'''
            for elite in range(self.NUMBER_OF_ELITES):
                # lists are mutable objects, we use [:] to return a copy
                new_population.append(self.population[elite][:])
            

            print("\nCrossover and Mutation Trace:")
            while new_population.__len__() < self.POPULATION_SIZE:
                parent1 = self.select_tournament(self.population)
                parent2 = self.select_tournament(self.population)


                child1, child2 = self.crossover_chromosomes(parent1, parent2)


                self.mutate_chromosome(child1)
                self.mutate_chromosome(child2)


                new_population.append(child1)

                # make sure to not depass the population size if we keep the elite
                if new_population.__len__() < self.POPULATION_SIZE:
                    new_population.append(child2)

            new_population.sort(key=lambda x: self._fitness(x), reverse=False)
            self.population = new_population

if __name__ == "__main__":
    # setup seed data
    data = [0, 1, 2, 3, 4, 5, 6, 7]
    ga = GeneticAlgorithm(data, max_weight=12210, max_volume=12, max_generations=60, population_size=200, elites=1) 

    ga.run()     # run the GA
    print(ga.printFittest()) 
    ga.printEvolutionGraph()
