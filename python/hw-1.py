import math

def print_type(variable):
    print("Type: ", type(variable))

def do_action(variable):
    if isinstance(variable, bool):
        print("Reverse bool: ", not variable, "\n")
    elif isinstance(variable, int):
        print("Square the number is:", variable*variable, "\n")
    elif isinstance(variable, float):
        print(variable, "+ pi = ", variable + math.pi, "\n")
    elif isinstance(variable, list):
        variable.reverse()
        print("Reverse list: ", variable, "\n")
    else:
        print("Wrong type")

variables = [ 42, 45.0, True, False, [16, 9, 43, 65, 97, 0]]

for variable in variables:
    print("Variable is ",variable)
    print_type(variable)
    do_action(variable)
