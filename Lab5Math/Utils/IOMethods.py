from tabulate import tabulate

from Methods.MethodsUtils import methods_arr
from Model.Answer import Answer
from Model.TableFunction import TableFunction, function_types_arr, get_function_result
from Utils.Exceptions import exceptions_arr


# Выбрать, вводим на основе функции или таблицы
def get_data() -> TableFunction:
    print("Выберите способ задания исходных данных:")
    print("( 0 ) Ввод таблицы значений (x, y)")
    print("( 1 ) На основе выбранной функции")

    try:
        inp = input()
        if inp == "0":
            return get_table_data()
        elif inp == "1":
            return get_function_data()
        else:
            raise ValueError
    except ValueError:
        print("Ошибка: ", exceptions_arr['ValueError'])
        exit(1)


# Вводим табличные данные
def get_table_data():
    read_line = input

    def close_file():
        return None

    # Определение источника ввода данных
    print("( 0 ) Ввод из консоли")
    print("( 1 ) Ввод из файла")

    mode = input()
    try:
        if mode == "1":
            file_name = input('Введите имя файла: ')
            file = open(file_name, 'r')
            read_line = lambda x: file.readline()
            close_file = file.close
        elif mode != "0":
            raise ValueError
    except ValueError:
        print("Ошибка: ", exceptions_arr['WrongLimitsArgument'])
        exit(1)
    except FileNotFoundError or IOError:
        print('Ошибка: ', exceptions_arr['FileNotFound'])
        exit(1)

    # Ввод точек
    points = []
    n = 0
    try:
        if mode == "0":
            print("Для завершения ввода - нажмите ENTER")
        print('Введите координаты точек построчно:')
        while True:
            line = read_line('').strip().lower()
            if len(line) == 0:
                break
            point_arr = list(line.split())
            if len(point_arr) > 2:
                print('Ошибка: ', exceptions_arr['TooMuchArguments'])
                close_file()
                exit(1)

            x = float(point_arr[0].replace(',', '.'))
            y = float(point_arr[1].replace(',', '.'))
            points.append((x, y))
            n += 1

    except ValueError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        close_file()
        exit(1)
    except IndexError:
        print('Ошибка: ', exceptions_arr['TooLittleArguments'])
        close_file()
        exit(1)

    close_file()

    points = sorted(points)
    x_arr = []
    y_arr = []
    for i in range(len(points)):
        x_arr.append(points[i][0])
        y_arr.append(points[i][1])
    return TableFunction(n, x_arr, y_arr)


def get_function_data():

    # Определяем функцию
    print("Выберите функцию из списка:")
    for i in range(len(function_types_arr)):
        print("(", i, ")", function_types_arr[i])
    func_type = input()
    try:
        func_type = int(func_type)
        if func_type >= len(function_types_arr) or func_type < 0:
            print("Ошибка: ", exceptions_arr['WrongLimitsArgument'])
            exit(1)
    except ValueError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        exit(1)

    # Задаем интервал для узлов
    interval = input("Введите границы отрезка через пробел (пример: 0 3): ").strip().split()
    a = None
    b = None
    try:
        if len(interval) > 2:
            print('Ошибка: ', exceptions_arr['TooMuchArguments'])
            exit(1)

        a = float(interval[0].replace(',', '.'))
        b = float(interval[1].replace(',', '.'))
        if a > b:
            a, b = b, a
        if func_type == 0 and a < 0:
            raise ArithmeticError

    except ArithmeticError:
        print('Ошибка: ', exceptions_arr['SqrtErrorInterval'])
        exit(1)
    except ValueError or IndexError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        exit(1)

    n = input("Введите количество узлов интерполяции: ")
    try:
        n = int(n)
        if n < 2:
            print('Ошибка: ', exceptions_arr['TooLittleN'])
            exit(1)
    except ValueError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        exit(1)

    # Формируем табличные данные
    x_arr = []
    y_arr = []
    h = (b - a) / (n - 1)
    x_curr = a
    for i in range(n):
        y_curr = get_function_result(func_type, x_curr)
        if y_curr is not None:
            y_arr.append(y_curr)
            x_arr.append(x_curr)
        x_curr += h

    if len(x_arr) < 2:
        print('Ошибка: ', exceptions_arr['TooLittleN'])
        exit(1)

    return TableFunction(n, x_arr, y_arr)


def get_method() -> int:
    print("Выберите метод для решения:")
    for i in range(len(methods_arr)):
        print("(", i, ")", methods_arr[i])

    method_type = input()
    try:
        method_type = int(method_type)
        if method_type >= len(methods_arr) or method_type < 0:
            print("Ошибка: ", exceptions_arr['WrongLimitsArgument'])
            exit(1)
    except ValueError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        exit(1)

    return method_type


def get_x(table_function: TableFunction) -> float:
    x = input("Введите x, для которого нужно найти y: ").strip().replace(',', '.')
    try:
        x = float(x)
        if x < table_function.x_arr[0] or x > table_function.x_arr[len(table_function.x_arr) - 1]:
            print('Ошибка: ', exceptions_arr['XIsOutOfInterval'])
            exit(1)
    except ValueError:
        print('Ошибка: ', exceptions_arr['ValueError'])
        exit(1)
    return x


def print_answer(answer: Answer):
    if not answer.ok:
        print(answer.message)
    else:
        print("y = ", answer.answer)


def print_answers(answers: list[Answer]):
    for i in range(len(answers)):
        print("---------------------------")
        print(methods_arr[i], ":")
        if not answers[i].ok:
            print(answers[i].message)
        else:
            print("y = ", answers[i].answer)
            if answers[i].message != "":
                print("Note:", answers[i].message)


def print_table_points(table_function: TableFunction):
    table = []
    headers = ['X', 'Y']
    for i in range(len(table_function.x_arr)):
        table.append([table_function.x_arr[i], table_function.y_arr[i]])
    print("---------------------------")
    print("Таблица узловых точек:")
    print(tabulate(table, headers, tablefmt="github"))


def print_table_lambda(lambda_table):
    print("---------------------------")
    print("Таблица конечных разностей:")
    headers = ['y']
    for i in range(len(lambda_table)):
        headers.append('y_' + str(i + 1))
    print(tabulate(lambda_table, headers, tablefmt="github"))
