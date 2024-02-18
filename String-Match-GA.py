import random
import string
import matplotlib.pyplot as plt


# Function to randomly generate an initial population with a set string length
def generate_population(population_size, string_length, gene_pool):
    initial_population = []
    gene_pool_list = sorted(list(gene_pool))
    for _ in range(population_size):
        individual = ''.join(random.sample(gene_pool_list, string_length))
        initial_population.append(individual)
    return initial_population


# Function to calculate fitness of an individual in a population and store them in an array
def calculate_fitness_scores(population, target_string, penalty=0):
    fitness_scores = []
    for individual in population:
        score = 0
        for i, char in enumerate(individual): # Numerate all characters in an individual string to iterate through them
            if i < len(target_string) and char == target_string[i]:
                score += 1
            else:
                score -= penalty
        fitness_scores.append(score / len(target_string))
    return fitness_scores


# Simple function that mutates a random character in a child, based on rng
def mutation(child, mutation_rate, gene_pool):
    mutated_child = ''
    for char in child:
        if random.random() < mutation_rate:
            mutated_child += random.choice(list(gene_pool))
        else:
            mutated_child += char
    return mutated_child


# Tournament selection that takes a population and selects a set of individuals and picks the one with the best score
def tournament_selection(population, fitness_scores, tournament_size):
    selected_parents = []
    population_fitness = list(zip(population, fitness_scores))  # create a list of tuples with individual and their fitness score
    for _ in range(len(population)):
        tournament = random.choices(population_fitness, k=tournament_size)
        winner = max(tournament, key=lambda x: x[1]) # Picks the highest fitness from the tournament
        selected_parents.append(winner[0])
    return selected_parents


# Function to perform uniform crossover based on rng
def uniform_crossover(parent1, parent2, crossover_rate):
    child1 = ''
    child2 = ''

    for char1, char2 in zip(parent1, parent2):
        if random.random() < crossover_rate:
            child1 += char1
            child2 += char2
        else:
            child1 += char1
            child2 += char2

    return child1, child2


# Function to perform genetic algorithm
def perform_genetic_algorithm(population, target_string, max_generations, mutation_rate, crossover_rate, gene_pool):
    fitness = [] # Empty array to store best fitness from each generation

    for generation in range(max_generations): # For loop to continue algorithm as long as current generation is below max
        fitness_scores = calculate_fitness_scores(population, target_string)

        # Termination criteria
        if max(fitness_scores) == 1:
            best_individual_index = fitness_scores.index(max(fitness_scores))
            best_individual = population[best_individual_index]
            print(f"Best individual found in generation {generation + 1}: {best_individual}")
            break
        if generation == max_generations - 1:
            print(f"Maximum generations reached")
            break

        # Find the most fit individual from this generation and add the fitness score to the array
        fittest_idx = fitness_scores.index(max(fitness_scores))
        fittest_individual = population[fittest_idx]
        fitness.append(max(fitness_scores))

        print(f"Generation {generation + 1}, Fittest individual: {fittest_individual}, Fitness: {fitness[-1]}")

        # Start performing GA stuff
        selected_parents = tournament_selection(population, fitness_scores, 5)

        new_population = []
        for i in range(0, len(selected_parents), 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i + 1]

            # From the selected parents perform crossover and mutation
            child1, child2 = uniform_crossover(parent1, parent2, crossover_rate)

            child1 = mutation(child1, mutation_rate, gene_pool)
            child2 = mutation(child2, mutation_rate, gene_pool)

            new_population.extend([child1, child2])

        population = new_population

    plt.plot(range(1, len(fitness) + 1), fitness)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness Progress over Generations')
    plt.show()


# Create a gene pool of accepted characters
gene_pool = set(string.ascii_uppercase)
gene_pool.update(string.digits)
gene_pool.update(['_', '*', '@', '.', ',', '^', '#'])

# Define parameters for algorithm
population_size = 50
max_generations = 1000
mutation_rate = 0.01
crossover_rate = 0.75

# Goal for algorithm
target_string = "MAGNUS_MORTENSEN*581813"

# Generate an initial population
population = generate_population(population_size, len(target_string), gene_pool)

perform_genetic_algorithm(population, target_string, max_generations, mutation_rate, crossover_rate, gene_pool)
