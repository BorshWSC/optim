import random
import time
import tkinter as tk
from functools import partial
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx

COUNT = 200
EDGE_CHANCE = 0.20

graph = erdos_renyi_graph(COUNT, EDGE_CHANCE)


def prepare_matrix():
    matrix = np.array(nx.to_scipy_sparse_matrix(graph).todense())
    matrix[matrix == 0] = 1_000_000
    np.fill_diagonal(matrix, 0)
    print(matrix)
    return matrix


def calculate_path(i, g, n, k):
    for j in range(n):
        g[i][j] = min(g[i][j], g[i][k] + g[k][j])
    return i, g[i]


def floyd_async(matrix):
    start_time = time.time()
    n = matrix.shape[0]
    pool = Pool()
    for k in range(n):
        p = partial(calculate_path, g=matrix, n=n, k=k)
        result_list = pool.map(p, range(n))
        for result in result_list:
            matrix[result[0]] = result[1]
    pool.close()
    pool.join()
    print(f'Время асинхронного выполнения: {time.time() - start_time}')
    return matrix


def floyd(matrix):
    start_time = time.time()
    n = matrix.shape[0]
    for r in range(n):
        for p in range(n):
            for q in range(n):
                matrix[p][q] = min(matrix[p][q], matrix[p][r] + matrix[r][q])
    print(f'Время синхронного выполнения: {time.time() - start_time}')


def generate_graph():
    for _, __, w in graph.edges(data=True):
        w['weight'] = random.randint(50, 200)


def draw_window(window):
    tk.Canvas(window)
    window.title("Task1")
    figure = plt.figure(figsize=(16, 9), dpi=100)
    ax = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.get_tk_widget().grid(row=1, column=0)
    canvas.draw()

    button = tk.Button(master=window, text="Calculate graph",
                       command=lambda: calculate_short(canvas, ax))
    button.grid(row=0, column=0)

    return canvas, ax


def calculate_short(canvas, ax):
    matrix = prepare_matrix()
    _async = floyd_async(matrix)
    floyd(matrix)
    redraw_graph(matrix, canvas, ax)


def redraw_graph(matrix, canvas, ax):
    matrix[matrix == 1_000_000] = 0
    ax.clear()
    g = nx.from_numpy_matrix(matrix)
    pos = nx.spring_layout(g)
    nx.draw(g, pos, ax=ax, with_labels=False)
    canvas.draw()


def draw_graph(canvas, ax):
    ax.clear()
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, ax=ax)
    canvas.draw()


def main():
    window = tk.Tk()
    canvas, ax = draw_window(window)
    canvas.draw()

    generate_graph()
    draw_graph(canvas, ax)
    window.mainloop()


if __name__ == '__main__':
    main()
