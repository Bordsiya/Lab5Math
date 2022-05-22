from Model.Answer import Answer
from Model.TableFunction import TableFunction
from Utils.MathMethods import get_factorial


def newton_interpolation(table_function: TableFunction, x: float, lambda_table) -> Answer:
    message = ""
    if table_function.n < 2:
        return Answer(False, "Количество узлов слишком мало", 0)
    is_equally_spaced = True
    h = round(table_function.x_arr[1] - table_function.x_arr[0], 3)

    # проверяем, равноотстоящие ли узлы
    for i in range(1, table_function.n - 1):
        if round(table_function.x_arr[i + 1] - table_function.x_arr[i], 3) != h:
            is_equally_spaced = False
            break

    if not is_equally_spaced:
        # неравноотстоящие узлы
        # ищем индекс x_i <= x
        return Answer(False, "Неравноотстоящие узлы", 0)
    else:
        # равноотстоящие узлы
        x_middle = (table_function.x_arr[0] + table_function.x_arr[table_function.n - 1]) / 2
        if x > x_middle:
            # интерполирование назад
            t = (x - table_function.x_arr[table_function.n - 1]) / h
            n = lambda_table[table_function.n - 1][0]
            for i in range(1, table_function.n):
                comp_t = 1
                curr_t = t
                for j in range(i):
                    comp_t *= curr_t
                    curr_t += 1
                n += comp_t * lambda_table[table_function.n - i - 1][i] / get_factorial(i)
            return Answer(True, message, n)
        else:
            # интерполирование вперед
            # ищем левую границу интервала для x
            x_left_ind = None
            for i in range(0, table_function.n - 1):
                if (x > table_function.x_arr[i]) and (x < table_function.x_arr[i + 1]):
                    x_left_ind = i
                    break
                elif x == table_function.x_arr[i]:
                    return Answer(True, "", table_function.y_arr[i])
                elif x == table_function.x_arr[i + 1]:
                    return Answer(True, "", table_function.y_arr[i + 1])
            if x_left_ind is None:
                message = "Переданный x находится вне промежутка"
                if x > table_function.x_arr[len(table_function.x_arr) - 1]:
                    x_left_ind = len(table_function.x_arr) - 1
                else:
                    x_left_ind = 0

            t = (x - table_function.x_arr[x_left_ind]) / h
            n = lambda_table[x_left_ind][0]
            for i in range(1, table_function.n - x_left_ind):
                comp_t = 1
                curr_t = t
                for j in range(i):
                    comp_t *= curr_t
                    curr_t -= 1
                n += comp_t * lambda_table[x_left_ind][i] / get_factorial(i)
            return Answer(True, message, n)
