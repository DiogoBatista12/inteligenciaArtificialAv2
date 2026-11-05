"""Visualização opcional da solução usando Tkinter (já incluso no Python)."""

import tkinter as tk
from tkinter import messagebox
from puzzle import GOAL, apply_move, format_board

def animate_solution(start, moves):
    root = tk.Tk()
    root.title("8-Puzzle - Solução pelo Algoritmo Genético")
    root.resizable(False, False)

    board = start
    index = 0
    title = tk.Label(root, text="Tabuleiro inicial", font=("Arial", 16, "bold"))
    title.pack(pady=10)

    grid = tk.Frame(root)
    grid.pack(padx=15, pady=10)
    cells = []
    for r in range(3):
        row = []
        for c in range(3):
            label = tk.Label(
                grid, text="", width=5, height=2,
                font=("Arial", 24, "bold"),
                relief="ridge", borderwidth=2, bg="white"
            )
            label.grid(row=r, column=c, padx=3, pady=3)
            row.append(label)
        cells.append(row)

    status = tk.Label(root, text="", font=("Arial", 11))
    status.pack(pady=5)

    def draw():
        for i, value in enumerate(board):
            r, c = divmod(i, 3)
            cells[r][c].config(text="" if value == 0 else str(value),
                               bg="#dbeafe" if value else "#e5e7eb")
        status.config(text=f"Movimento {index} de {len(moves)}")

    def next_move():
        nonlocal board, index
        if index >= len(moves):
            messagebox.showinfo("Fim", "Sequência concluída!")
            return
        board = apply_move(board, moves[index])
        index += 1
        title.config(text=f"Movimento: {moves[index-1]}")
        draw()
        if index < len(moves):
            root.after(650, next_move)
        else:
            root.after(650, lambda: title.config(text="Objetivo alcançado!" if board == GOAL else "Sequência concluída"))

    draw()
    if moves:
        root.after(650, next_move)
    else:
        title.config(text="O tabuleiro já estava resolvido!")
    tk.Button(root, text="Fechar", command=root.destroy).pack(pady=10)
    root.mainloop()
