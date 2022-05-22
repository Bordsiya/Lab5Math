import os

import matplotlib.pyplot as plt
import numpy as np

from Methods.MethodsUtils import do_method, methods_colors, methods_polynom_labels, methods_img_names
from Model.Answer import Answer
from Model.TableFunction import TableFunction


def get_polynomial(method_id: int, table_function: TableFunction, x_left: float, x_right: float):
    y_arr = []
    x_arr = []
    x_arr_linspace = np.linspace(x_left - 0.2, x_right + 0.2, len(table_function.x_arr) * 5)
    for i in range(len(x_arr_linspace)):
        ans = do_method(method_id, table_function, x_arr_linspace[i])
        if ans.ok:
            y_arr.append(ans.answer)
            x_arr.append(x_arr_linspace[i])
    return x_arr, y_arr


def draw_graphs(table_function: TableFunction, x: float, answers: list[Answer]):
    graphs_img_name = "graphs_interpolation"

    if os.path.exists('/' + graphs_img_name):
        os.remove('/' + graphs_img_name)
    for i in range(len(answers)):
        if os.path.exists('/' + methods_img_names[i]):
            os.remove('/' + methods_img_names[i])

    plt.cla()
    plt.clf()
    plt.gcf().canvas.set_window_title("График интерполяций")
    plt.grid()
    axes = plt.gca()

    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['left'].set_position('zero')
    axes.spines['bottom'].set_position('zero')
    axes.set_xlabel('x', loc='right')
    axes.set_ylabel('y', loc='top')
    axes.plot(1, 0, marker=">", ms=5, color='k', transform=axes.get_yaxis_transform(), clip_on=False)
    axes.plot(0, 1, marker="^", ms=5, color='k', transform=axes.get_xaxis_transform(), clip_on=False)

    # табличные точки
    X = table_function.x_arr
    Y = table_function.y_arr
    # plt.xticks(np.arange(min(X), max(X) + 1, 1.0))
    axes.scatter(X, Y)

    # точки вычисленные методами
    y_arr = []
    for i in range(len(answers)):
        if answers[i].ok:
            y_arr.append(answers[i].answer)
            axes.scatter(x, answers[i].answer, marker='x', color=methods_colors[i], label=methods_polynom_labels[i])

    # полиномы
    specified_x_arr = [[]] * len(answers)
    specified_y_arr = [[]] * len(answers)

    for i in range(len(answers)):
        if answers[i].ok:
            x_arr_new, y_arr = \
                get_polynomial(i, table_function, table_function.x_arr[0],
                               table_function.x_arr[len(table_function.x_arr) - 1])
            axes.plot(x_arr_new, y_arr, color=methods_colors[i], label=methods_polynom_labels[i])
            specified_x_arr[i] = x_arr_new
            specified_y_arr[i] = y_arr

    axes.legend()
    plt.savefig(graphs_img_name)

    for i in range(len(answers)):
        if answers[i].ok:
            draw_graph_specified(i, specified_x_arr[i], specified_y_arr[i], table_function, x, answers[i])


def draw_graph_specified(method_id: int, x_arr: list[float], y_arr: list[float], table_function: TableFunction,
                         x: float, answer: Answer):
    plt.cla()
    plt.clf()
    plt.gcf().canvas.set_window_title("График интерполяций")
    plt.grid()

    axes = plt.gca()

    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['left'].set_position('zero')
    axes.spines['bottom'].set_position('zero')
    axes.set_xlabel('x', loc='right')
    axes.set_ylabel('y', loc='top')
    axes.plot(1, 0, marker=">", ms=5, color='k', transform=axes.get_yaxis_transform(), clip_on=False)
    axes.plot(0, 1, marker="^", ms=5, color='k', transform=axes.get_xaxis_transform(), clip_on=False)

    # табличные точки
    X = table_function.x_arr
    Y = table_function.y_arr
    # plt.xticks(np.arange(min(X), max(X) + 1, 1.0))
    axes.scatter(X, Y)

    # вычисленный y
    axes.scatter(x, answer.answer, marker='x', color=methods_colors[method_id], label=methods_polynom_labels[method_id])

    axes.plot(x_arr, y_arr, color=methods_colors[method_id], label=methods_polynom_labels[method_id])

    axes.legend()
    plt.savefig(methods_img_names[method_id])
