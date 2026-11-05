from puzzle import DEFAULT_START, GOAL, format_board, is_solvable
from genetic_algorithm import GeneticAlgorithm, GAConfig
from visualizer import animate_solution

def read_board():
    print("Digite os 9 números do tabuleiro inicial, usando 0 para o espaço vazio.")
    print("Exemplo: 1 2 3 4 0 6 7 5 8")
    while True:
        try:
            values = list(map(int, input("> ").split()))
            if len(values) != 9 or sorted(values) != list(range(9)):
                raise ValueError
            board = tuple(values)
            if not is_solvable(board):
                print("Esse tabuleiro não possui solução. Tente novamente.")
                continue
            return board
        except ValueError:
            print("Entrada inválida. Digite cada número de 0 a 8 exatamente uma vez.")

def main():
    print("=" * 58)
    print("       JOGO DOS 8 NÚMEROS - ALGORITMO GENÉTICO")
    print("=" * 58)
    print("\n1 - Usar tabuleiro de demonstração")
    print("2 - Informar meu próprio tabuleiro")
    choice = input("Escolha: ").strip()
    start = DEFAULT_START if choice != "2" else read_board()

    print("\nTabuleiro inicial:")
    print(format_board(start))
    print("\nObjetivo:")
    print(format_board(GOAL))

    config = GAConfig()
    print("\nParâmetros do AG:")
    print(f"População: {config.population_size}")
    print(f"Gerações máximas: {config.generations}")
    print(f"Taxa de cruzamento: {config.crossover_rate:.0%}")
    print(f"Taxa de mutação: {config.mutation_rate:.0%}")
    print(f"Elitismo: {config.elite_size}")

    print("\nExecutando o algoritmo genético...")
    ga = GeneticAlgorithm(config)
    result = ga.solve(start, verbose=True)

    print("\n" + "=" * 58)
    if result.solved:
        print("SOLUÇÃO ENCONTRADA!")
        print(f"Movimentos: {len(result.moves)}")
        print(f"Geração: {result.generation}")
        print(f"Tempo: {result.elapsed:.4f} segundos")
        print(f"Melhor fitness: {result.fitness:.6f}")
        print("\nSequência:", " -> ".join(result.moves) if result.moves else "(já estava resolvido)")
        print("\nTabuleiro final:")
        print(format_board(result.final_board))
        save = input("\nDeseja visualizar a sequência no tabuleiro? (s/n): ").lower()
        if save == "s":
            animate_solution(start, result.moves)
    else:
        print("O AG não encontrou a solução dentro do limite configurado.")
        print(f"Melhor distância Manhattan: {result.distance}")
        print(f"Gerações executadas: {result.generation}")
        print(f"Tempo: {result.elapsed:.4f} segundos")
        print("Tente aumentar gerações/população em genetic_algorithm.py ou usar outro seed.")
    print("=" * 58)

if __name__ == "__main__":
    main()
