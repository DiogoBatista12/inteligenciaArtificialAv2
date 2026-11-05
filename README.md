# 8-Puzzle com Algoritmo Genético (AG)

Projeto acadêmico em Python que aplica um Algoritmo Genético ao Jogo dos 8 Números.

## Objetivo

Encontrar uma sequência de movimentos do espaço vazio (`CIMA`, `BAIXO`, `ESQUERDA`, `DIREITA`) que transforme o tabuleiro inicial no estado objetivo:

```text
1 2 3
4 5 6
7 8 0
```

O número `0` representa o espaço vazio.

## Requisitos

- Python 3.10 ou superior.
- Não utiliza bibliotecas externas.
- Tkinter é opcional e normalmente acompanha a instalação do Python no Windows.

## Como executar

Abra o terminal dentro da pasta do projeto e execute:

```bash
python main.py
```

Escolha `1` para usar o tabuleiro de demonstração ou `2` para informar outro tabuleiro.

Exemplo de entrada:

```text
1 2 3 4 0 6 7 5 8
```

Digite os nove valores separados por espaço. O `0` representa o espaço vazio.

## Como o Algoritmo Genético funciona neste projeto

1. **Representação:** cada indivíduo (cromossomo) é uma sequência de movimentos.
2. **População inicial:** são criadas sequências aleatórias.
3. **Fitness:** cada sequência é simulada; a aptidão considera a menor distância Manhattan alcançada durante a sequência. Quanto menor a distância, maior o fitness.
4. **Seleção:** torneio, escolhendo o melhor entre alguns indivíduos sorteados.
5. **Cruzamento:** cruzamento de um ponto, combinando partes de dois pais.
6. **Mutação:** cada gene pode ser substituído por um movimento aleatório.
7. **Elitismo:** os melhores indivíduos passam diretamente para a próxima geração.

A distância Manhattan soma, para cada peça, quantas casas ela precisa andar na horizontal e na vertical para chegar à posição final.

## Parâmetros

Os parâmetros ficam na classe `GAConfig`, em `genetic_algorithm.py`:

| Parâmetro | Padrão | Significado |
|---|---:|---|
| `population_size` | 180 | Quantidade de indivíduos por geração |
| `generations` | 1200 | Limite de gerações |
| `chromosome_length` | 24 | Quantidade de genes por indivíduo |
| `crossover_rate` | 0.85 | Probabilidade de cruzamento |
| `mutation_rate` | 0.12 | Probabilidade de mutação por gene |
| `elite_size` | 8 | Indivíduos preservados |
| `tournament_size` | 4 | Participantes de cada torneio |
| `random_seed` | 42 | Semente para repetir os experimentos |

## Visualização

Se a solução for encontrada, o programa pergunta se deseja abrir uma animação do tabuleiro. A animação usa Tkinter.

## Limitações importantes para o relatório

- O AG é probabilístico: não garante encontrar uma solução em todas as execuções.
- A solução encontrada não é necessariamente a de menor número de movimentos.
- A instância padrão é curta, adequada para demonstrar o funcionamento. Para experimentos, altere o tabuleiro e os parâmetros.
- O fitness deste projeto avalia o melhor estado visitado por cada sequência, e não apenas o último estado.
- Movimentos ilegais são ignorados durante a simulação.

## Estrutura

```text
8puzzle_ag/
├── main.py
├── puzzle.py
├── genetic_algorithm.py
├── visualizer.py
├── README.md
└── resultados/
```

## Ideias para os experimentos

Execute o programa várias vezes mudando `random_seed`, população, mutação e gerações. Registre:

- se encontrou a solução;
- número de gerações;
- tempo de execução;
- quantidade de movimentos;
- distância Manhattan final.

Use esses dados para discutir o efeito dos parâmetros do AG.
