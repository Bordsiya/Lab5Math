from Methods.MethodsUtils import do_methods, create_table_lambdas
from Utils.GraphMethods import draw_graphs
from Utils.IOMethods import get_data, get_x, print_answers, print_table_points, print_table_lambda

table_function = get_data()
x = get_x(table_function)
answers = do_methods(table_function, x)
print_table_points(table_function)
print_table_lambda(create_table_lambdas(table_function))
draw_graphs(table_function, x, answers)
print_answers(answers)
