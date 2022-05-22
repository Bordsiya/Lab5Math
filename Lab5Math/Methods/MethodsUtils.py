from Methods.Bessellnterpolation import bessel_interpolation
from Methods.LagrangeInterpolation import langrange_interpolation
from Methods.NewtonInterpolation import newton_interpolation
from Methods.StirlingInterpolation import stirling_interpolation
from Model.Answer import Answer
from Model.TableFunction import TableFunction

methods_arr = [
    'Метод Бесселя',
    'Метод Лагранжа',
    'Метод Ньютона',
    'Метод Стирлинга'
]


methods_colors = [
    'b',
    'g',
    'r',
    'm'
]


methods_img_names = [
    'bessel_interpolation',
    'lagrange_interpolation',
    'newton_interpolation',
    'stirling_interpolation'
]


methods_polynom_labels = [
    'Полином Бесселя',
    'Полином Лагранжа',
    'Полином Ньютона',
    'Полином Стирлинга'
]


def do_method(method_id: int, table_function: TableFunction, x: float) -> Answer:
    lambda_table = create_table_lambdas(table_function)
    if method_id == 0:
        return bessel_interpolation(table_function, x, lambda_table)
    elif method_id == 1:
        return langrange_interpolation(table_function, x)
    elif method_id == 2:
        return newton_interpolation(table_function, x, lambda_table)
    else:
        return stirling_interpolation(table_function, x, lambda_table)


def do_methods(table_function: TableFunction, x: float) -> list[Answer]:
    answers = []
    for i in range(len(methods_arr)):
        answers.append(do_method(i, table_function, x))
    return answers


def create_table_lambdas(table_function: TableFunction):
    lambda_table = [[""] * len(table_function.x_arr) for i in range(len(table_function.x_arr))]
    get_lambda(len(table_function.x_arr) - 1, 0, table_function, lambda_table)
    return lambda_table


def get_lambda(k: int, ind: int, table_function: TableFunction, lambda_table):
    if k == 0:
        diff = table_function.y_arr[ind]
        lambda_table[ind][k] = diff
        return diff

    diff = get_lambda(k - 1, ind + 1, table_function, lambda_table) - get_lambda(k - 1, ind, table_function, lambda_table)
    lambda_table[ind][k] = diff
    return diff

