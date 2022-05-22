from Model.Answer import Answer
from Model.TableFunction import TableFunction
from Utils.MathMethods import get_factorial


def stirling_interpolation(table_function: TableFunction, x: float, lambda_table) -> Answer:
    message = ""
    if table_function.n < 2:
        return Answer(False, "Количество узлов слишком мало", 0)

    if table_function.n % 2 == 0:
        return Answer(False, "Нужно нечетное число узлов", 0)

    is_equally_spaced = True
    h = round(table_function.x_arr[1] - table_function.x_arr[0], 3)
    # проверяем, равноотстоящие ли узлы
    for i in range(1, table_function.n - 1):
        if round(table_function.x_arr[i + 1] - table_function.x_arr[i], 3) != h:
            is_equally_spaced = False
            break
    if not is_equally_spaced:
        return Answer(False, "Узлы неравноотстоящие", 0)

    # ищем узел x0 = a
    if table_function.n % 2 == 0:
        x_0 = int(table_function.n / 2 - 1)
    else:
        x_0 = int(table_function.n / 2)

    t = (x - table_function.x_arr[x_0]) / h
    if abs(t) > 0.25:
        message = "t <= 0.25"

    n = lambda_table[x_0][0]
    comp_t1 = t
    comp_t2 = t**2
    pred_number = 0

    for i in range(1, table_function.n):
        if i % 2 == 0:
            n += (comp_t2 / get_factorial(i)) * lambda_table[x_0 - (i // 2)][i]
            comp_t2 *= (t**2 - pred_number**2)
        else:
            n += (comp_t1 / get_factorial(i)) * \
                 ((lambda_table[x_0 - ((i + 1) // 2)][i] + lambda_table[x_0 - (((i + 1) // 2) - 1)][i]) / 2)
            pred_number += 1
            comp_t1 *= (t**2 - pred_number**2)
    return Answer(True, message, n)
