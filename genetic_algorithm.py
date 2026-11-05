"""Implementação didática de Algoritmo Genético para o 8-Puzzle."""

from dataclasses import dataclass
import random
import time

from puzzle import (
    GOAL, MOVE_NAMES, apply_move, legal_moves,
    manhattan_distance
)

@dataclass
class GAConfig:
    population_size: int = 180
    generations: int = 1200
    chromosome_length: int = 24
    crossover_rate: float = 0.85
    mutation_rate: float = 0.12
    elite_size: int = 8
    tournament_size: int = 4
    random_seed: int | None = 42
    report_every: int = 100

@dataclass
class GAResult:
    solved: bool
    moves: list
    final_board: tuple
    generation: int
    elapsed: float
    fitness: float
    distance: int

class GeneticAlgorithm:
    def __init__(self, config=None):
        self.config = config or GAConfig()
        self.rng = random.Random(self.config.random_seed)

    def _random_chromosome(self):
        return [self.rng.choice(MOVE_NAMES)
                for _ in range(self.config.chromosome_length)]

    def _evaluate(self, start, chromosome):
        """
        Simula o cromossomo e considera o melhor estado visitado.
        Assim, movimentos posteriores não apagam uma solução já alcançada.
        Fitness maior é melhor.
        """
        board = start
        best_distance = manhattan_distance(board)
        best_prefix = []
        path = []

        if board == GOAL:
            return 1_000_000.0, [], board, 0

        for move in chromosome:
            # Genes que tentam sair do tabuleiro são ignorados e não entram
            # na sequência final de movimentos válidos.
            if move not in legal_moves(board):
                continue
            board = apply_move(board, move)
            path.append(move)

            distance = manhattan_distance(board)
            if distance < best_distance:
                best_distance = distance
                best_prefix = path.copy()

            if board == GOAL:
                return 1_000_000.0, path.copy(), board, 0

        # Penaliza distância restante e, levemente, sequências longas.
        fitness = 1.0 / (1.0 + best_distance + 0.002 * len(best_prefix))
        best_board = self._replay_prefix(start, best_prefix)
        return fitness, best_prefix, best_board, best_distance

    @staticmethod
    def _replay_prefix(start, moves):
        board = start
        for move in moves:
            if move in legal_moves(board):
                board = apply_move(board, move)
        return board

    def _tournament(self, population, scored):
        candidates = self.rng.sample(range(len(population)),
                                     min(self.config.tournament_size, len(population)))
        winner = max(candidates, key=lambda i: scored[i][0])
        return population[winner][:]

    def _crossover(self, parent1, parent2):
        if self.rng.random() > self.config.crossover_rate:
            return parent1[:], parent2[:]
        if len(parent1) < 2:
            return parent1[:], parent2[:]
        point = self.rng.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def _mutate(self, chromosome):
        child = chromosome[:]
        for i in range(len(child)):
            if self.rng.random() < self.config.mutation_rate:
                child[i] = self.rng.choice(MOVE_NAMES)
        return child

    def solve(self, start, verbose=False):
        started = time.perf_counter()
        if start == GOAL:
            return GAResult(True, [], GOAL, 0, 0.0, 1_000_000.0, 0)

        population = [self._random_chromosome()
                      for _ in range(self.config.population_size)]
        best_global = None
        best_global_fitness = float("-inf")
        best_global_distance = 99
        best_global_moves = []
        best_generation = 0

        for generation in range(1, self.config.generations + 1):
            evaluated = [self._evaluate(start, chromosome)
                         for chromosome in population]
            scores = [item[0] for item in evaluated]

            generation_best_index = max(range(len(population)), key=lambda i: scores[i])
            generation_best = evaluated[generation_best_index]

            if generation_best[0] > best_global_fitness:
                best_global_fitness = generation_best[0]
                best_global_moves = generation_best[1]
                best_global_distance = generation_best[3]
                best_generation = generation

            if verbose and (generation == 1 or generation % self.config.report_every == 0):
                print(
                    f"Geração {generation:4d} | "
                    f"melhor distância: {best_global_distance:2d} | "
                    f"fitness: {best_global_fitness:.6f}"
                )

            if generation_best[0] >= 1_000_000.0:
                elapsed = time.perf_counter() - started
                moves = generation_best[1]
                return GAResult(True, moves, GOAL, generation, elapsed,
                                generation_best[0], 0)

            # Elitismo: preserva os melhores cromossomos.
            elite_indices = sorted(range(len(population)),
                                   key=lambda i: scores[i], reverse=True)
            new_population = [
                population[i][:]
                for i in elite_indices[:self.config.elite_size]
            ]

            while len(new_population) < self.config.population_size:
                parent1 = self._tournament(population, scores)
                parent2 = self._tournament(population, scores)
                child1, child2 = self._crossover(parent1, parent2)
                new_population.append(self._mutate(child1))
                if len(new_population) < self.config.population_size:
                    new_population.append(self._mutate(child2))

            population = new_population

        elapsed = time.perf_counter() - started
        final_board = self._replay_prefix(start, best_global_moves)
        return GAResult(
            final_board == GOAL,
            best_global_moves,
            final_board,
            best_generation,
            elapsed,
            best_global_fitness,
            manhattan_distance(final_board)
        )
