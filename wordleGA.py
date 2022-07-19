from enum import Enum
import math
import statistics
import EasyGA
import random

GAME_SOLUTION = "VAPOR"
GREEN_TILE_SCORE = 2
YELLOW_TILE_SCORE = 1

class Color(Enum):
  BLACK = 0
  YELLOW = 1
  GREEN = 2

#Transform the cell to a single number representing the data
def cellToVal(letter: str, color: Color=Color.BLACK) -> str:
  if(letter == ""):
    return -1
  letterVal = ord(letter.capitalize())-65
  if(color == Color.BLACK):
    return letterVal
  if(color == Color.YELLOW):
    return letterVal + 64
  if(color == Color.GREEN):
    return letterVal + 128


## Set up the problem space
inputs = [
  cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""),
  cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""),
  cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""),
  cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""), cellToVal(""),
]

# Generate the solution space ( 1 - 8938 )
solutions = []
with open('dict5.txt', 'r') as reader:
  for line in reader.readlines():
    solutions.append(line.strip().upper())
    solutions.sort()

#Score
def calculate_score(solution: str, guess: str) -> int:
  out = 0
  for idx, char in enumerate(guess):
    if(solution[idx] == char):
      out += GREEN_TILE_SCORE
      sol_list = list(solution)
      sol_list[idx] = '_'
      solution = ''.join(sol_list)
  for char in guess:
    if(solution.find(char) > -1):
      out += YELLOW_TILE_SCORE
  return out

def wordFromChromosome(chromosome: list) -> str:
  guessInt = 0
  for gene in chromosome:
    for input in inputs:
      guessInt += gene.value * input * 1800

  guessInt = math.floor(guessInt)% len(solutions)
  return solutions[guessInt]

# Translate the index guess into the guess and score it
# for GA fitness and future culling
def fitness_dick_in_your_mouth_lmao(chromosome: list) -> int:

  def loc_calc_score(solution):
    return calculate_score(solution, wordFromChromosome(chromosome))
  
  return statistics.mean(
    list(map( loc_calc_score, random.choices(solutions, weights=None, k=100)))
  )

#Create the Genetic Algorithm
ga = EasyGA.GA()

ga.fitness_function_impl = fitness_dick_in_your_mouth_lmao

ga.chromosome_length = 5
# ga.fitness_goal = 5*GREEN_TILE_SCORE
ga.population_size = 50
ga.generation_goal = 1000000
ga.chromosome_mutation_rate = 0.1
ga.gene_mutation_rate = 0.00101
# Cross genes by choosing random floats between the genes
# ga.crossover_individual_impl = EasyGA.crossover.Crossover.Individual.Arithmetic.average
# ga.mutation_population_impl = EasyGA.mutation.Mutation.Population.random_selection

# def custom_mutation(chromosome):
#   print("I'm mutating POG")
#   return EasyGA.mutation.Mutation.Individual.Arithmetic.average(chromosome, random.randint(0, len(chromosome)))
# ga.mutation_individual_impl = custom_mutation
# ga.adapt_population_flag = False
# ga.adapt_rate = 0

# Creates random genes utilizing the characters below
ga.gene_impl = lambda: random.uniform(0, 1)

# print(arrprintfitness([0]*12))
# print(arrprintfitness([0.5]*12))
# print(arrprintfitness([1]*12))
# print(arrprintfitness([0.3808854930271173, 0.01018074948814629,0.5823231386273678,0.2563043879739938,0.387768853581284]))
# print(arrprintfitness([0.5759840345744782,0.021606683423686546,0.6106271648014394,0.2818295383306282,0.7663486107774451,0.18678380210484624,0.2477057829338336,0.5677221138918507,0.5900660312332475,0.6161444332130938,0.3658969692366928,0.6998416446608431]))


while ga.active():
    # Evolve only a certain number of generations
    ga.evolve(50)

    # Print the current generation
    ga.print_generation()
    print("Current Word\t" + GAME_SOLUTION)
    # Print the best chromosome from that generations population
    ga.print_best_chromosome()
    # for chrome in ga.sort_by_best_fitness()
    printdis = []
    for chromosome in ga.sort_by_best_fitness():
      printdis.append(wordFromChromosome(chromosome))
    print(printdis)
    # If you want to show each population
    # ga.print_population()
    # To divide the print to make it easier to look at
    GAME_SOLUTION = random.choice(solutions)
    print('-'*75)