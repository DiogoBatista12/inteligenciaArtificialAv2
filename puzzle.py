"""Funções e regras do Jogo dos 8 Números (8-Puzzle)."""

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

# Instância curta de demonstração: solução conhecida em 2 movimentos.
DEFAULT_START = (1, 2, 3,
                 4, 0, 6,
                 7, 5, 8)

MOVE_NAMES = ("CIMA", "BAIXO", "ESQUERDA", "DIREITA")

def legal_moves(board):
    """Retorna os movimentos válidos do espaço vazio."""
    zero = board.index(0)
    row, col = divmod(zero, 3)
    moves = []
    if row > 0:
        moves.append("CIMA")
    if row < 2:
        moves.append("BAIXO")
    if col > 0:
        moves.append("ESQUERDA")
    if col < 2:
        moves.append("DIREITA")
    return moves

def apply_move(board, move):
    """Aplica um movimento ao espaço vazio. Retorna o novo tabuleiro."""
    zero = board.index(0)
    row, col = divmod(zero, 3)
    target = {
        "CIMA": zero - 3,
        "BAIXO": zero + 3,
        "ESQUERDA": zero - 1,
        "DIREITA": zero + 1,
    }.get(move)

    if move not in legal_moves(board):
        return board

    new_board = list(board)
    new_board[zero], new_board[target] = new_board[target], new_board[zero]
    return tuple(new_board)

def apply_sequence(start, moves):
    """Executa uma sequência, ignorando movimentos inválidos."""
    board = start
    for move in moves:
        board = apply_move(board, move)
    return board

def manhattan_distance(board):
    """Soma das distâncias Manhattan das peças (sem contar o espaço vazio)."""
    total = 0
    for index, value in enumerate(board):
        if value == 0:
            continue
        current_row, current_col = divmod(index, 3)
        goal_index = GOAL.index(value)
        goal_row, goal_col = divmod(goal_index, 3)
        total += abs(current_row - goal_row) + abs(current_col - goal_col)
    return total

def is_solvable(board):
    """Verifica a paridade das inversões; em tabuleiro 3x3 deve ser par."""
    numbers = [n for n in board if n != 0]
    inversions = sum(
        1 for i in range(len(numbers))
        for j in range(i + 1, len(numbers))
        if numbers[i] > numbers[j]
    )
    return inversions % 2 == 0

def format_board(board):
    rows = []
    for i in range(0, 9, 3):
        row = [str(x) if x != 0 else " " for x in board[i:i+3]]
        rows.append("+---+---+---+")
        rows.append("| " + " | ".join(row) + " |")
    rows.append("+---+---+---+")
    return "\n".join(rows)
