from Model.Answer import Answer
from Model.TableFunction import TableFunction


def langrange_interpolation(table_function: TableFunction, x: float) -> Answer:
    if table_function.n < 2:
        return Answer(False, "Количество узлов слишком мало", 0)
    L_arr = []
    for i in range(table_function.n):
        comp_1 = 1
        comp_2 = 1
        for j in range(table_function.n):
            if i != j:
                comp_1 *= (x - table_function.x_arr[j])
                comp_2 *= (table_function.x_arr[i] - table_function.x_arr[j])
        l = comp_1 / comp_2
        L_arr.append(l * table_function.y_arr[i])

    return Answer(True, "", sum(L_arr))