
import sys


OPERATORS = "+-*/^()"

def print_history(history):
    print("\n\nHistory:")
    for action, mat, args in history:
        print("Action:", action % args)
        print_mat(mat)
        print()

def print_mat(mat):
    column_entry_length = []
    for column in range(len(mat[0])):
        column_entry_length.append(max([mat[row][column] for row in range(len(mat))], key=len))
    column_entry_length = list(map(len, column_entry_length))

    for i, row in enumerate(mat):
        print(i + 1, "", end="")
        if i == 0:
            print("┌ ", end="")
        elif i == len(mat) - 1:
            print("└ ", end="")
        else:
            print("│ ", end="")

        for j, value in enumerate(row):
            padding = " " * (column_entry_length[j] - len(value) + 1)
            if j != 0:
                padding += "   "
            print(padding + value, end="")

        if i == 0:
            print(" ┐")
        elif i == len(mat) - 1:
            print(" ┘")
        else:
            print(" │")

def get_int_input(quest, r=None):
    answer = ""
    i:int = 0
    while not answer:
        answer = input(quest)
        try:
            i = int(answer)
        except (TypeError, ValueError):
            answer = ""
        if r is not None and i not in r:
            answer = ""

    return i

def save_input(quest):
    answer = ""
    while not answer:
        answer = input(quest)
    return answer

def mat_copy(m):
    return [x[:] for x in m]

def math_expr(s):
    for op in OPERATORS:
        if op in s:
            return "(" + s + ")"
    return s

ARGS = sys.argv[1:]
mode = "g"
if not ARGS:
    answer = input("Mode: [G]aussian (default) / [i]nvert permutation: ")
    if answer.lower() == "i":
        mode = "i"
    else:
        mode = "g"
else:
    mode = ARGS[0].lower()[0]
    mode = "i" if mode == "i" else "g"


ROWS = get_int_input("Rows: ")
COLUMNS = get_int_input("Columns: ")

longest_value_length = 0

matrix = [[""] * COLUMNS for _ in range(ROWS)] 

for r in range(ROWS):
    for c in range(COLUMNS):
        value = ""
        while not value:
            value = save_input("Entry at %sr %sc: " % (r + 1, c + 1))
        matrix[r][c] = value

print("\nEntered matrix:")
print_mat(matrix)
print("\n")

if mode == "g":
    result_vec = [save_input("Result for row %i: " % (i + 1)) for i in range(ROWS)]

for i, row in enumerate(matrix):
    if mode == "i":
        perm_ext = ["0"] * ROWS
        perm_ext[i] = "1"
        row += ["|"] + perm_ext
    else:
        row += ["|", result_vec[i]]

swap_mapping_rows = {x: x for x in range(0, ROWS)}
history = [("start", mat_copy(matrix), ())]
ACTION_MAP = {
    "s": "swapped rows %s and %s",
    "~": "swapped rows %s and %s",
    "+": "add rows %s + %s",
    "a": "add rows %s + %s",
    "-": "subtract rows %s - %s",
    "w": "Add row with factor: %sr + %s * %sr",
    "m": "Multiply row %s with factor %s",
    "*": "Multiply row %s with factor %s",
    "e": "Edit value %sr %sc to value %s",
    "c": "swap columns",
}
while True:
    print("\n\n")
    print_mat(matrix)
    args = ()
    action = save_input("[S]wap/Swap [c]olumn/[A]dd/Subtract[-]/Add [w]ith factor/[M]ultiply/[E]dit value/[U]ndo/[H]istory/[Q]uit: ").lower()
    if not action:
        continue
    try:
        if action[0] == "q":
            if save_input("You sure to quit? [y]es/[N]o: ").lower() == "y":
                break
            continue

        elif action[0] == "e":
            print("NOTE: This operation can break the data validation (assuming you have no mistakes in your calculations so far... hehe")
            row = get_int_input("Row: ", range(1, ROWS + 1)) - 1
            column = get_int_input("Column: ", range(1, 2 * COLUMNS + 1)) - 1
            value = save_input("Enter value: ")
            matrix[row][column] = value
            args = (row + 1, column + 1, matrix[row][column])

        elif action[0] == "h":
            if len(history) == 1:
                print("No history with changes")
            else:
                print_history(history)

            continue

        elif action[0] == "u":
            if save_input("Really undo? [y]es/[N]o").lower() == "y":
                matrix = mat_copy(history[-1][1])
                history = history[:-1]

            continue

        elif action[0] in "s~":
            r1 = get_int_input("Row A to swap: ", range(1, ROWS + 1)) - 1
            r2 = get_int_input("Row B to swap: ", range(1, ROWS + 1)) - 1
            matrix[r1], matrix[r2] = matrix[r2], matrix[r1]
            swap_mapping_rows[r1] = r2
            swap_mapping_rows[r2] = r1
            args = (r1 + 1, r2 + 1)

        elif action[0] == "c":
            c1 = get_int_input("Column A to swap: ", range(1, COLUMNS + 1)) - 1
            c2 = get_int_input("Column B to swap: ", range(1, COLUMNS + 1)) - 1

            for row in matrix:
                row[c1], row[c2] = row[c2], row[c1]

            print("NOTE: The result vector has to be changed in the according rows")

        elif action[0] in "m*":
            row = get_int_input("Row to multiply with a factor: ", range(1, ROWS + 1)) - 1
            factor = save_input("Factor to multiply with: ")

            for i, value in enumerate(matrix[row][:COLUMNS]):
                result = save_input("Column %i: %s * %s = " % (i + 1, math_expr(value), math_expr(factor)))
                matrix[row][i] = result

            for i, value in enumerate(matrix[row][COLUMNS + 1:]):
                row_change = save_input("Result of %s * %s = " % (math_expr(value), math_expr(factor)))
                matrix[row][COLUMNS + 1 + i] = row_change

            args = (row + 1, factor)

        elif action[0] in "a+-":
            sign = "+" if action[0] in "a+" else "-"
            verb = "add" if action[0] in "a+" else "subtract (b in a-b)"
            target_row = get_int_input("Target row (which will be changed): ", range(1, ROWS + 1)) - 1
            row_to_add = get_int_input("Row to %s: " % verb, range(1, ROWS + 1)) - 1

            for i, (target_value, add_value) in enumerate(zip(matrix[target_row][:COLUMNS], matrix[row_to_add][:COLUMNS])):
                result = save_input("Column %i: %s %s %s = " % (i + 1, math_expr(target_value), sign, math_expr(add_value)))
                matrix[target_row][i] = result
            
            original_add_row = swap_mapping_rows[row_to_add]
            for i, value in enumerate(matrix[target_row][COLUMNS + 1:]):
                result = save_input("Result of %s %s %s = " % (value, sign, math_expr(matrix[row_to_add][COLUMNS + i + 1])))
                matrix[target_row][COLUMNS + i + 1] = result

            args = (row_to_add + 1, target_row + 1)

        elif action[0] == "w":
            target_row = get_int_input("Target row A (which will be changed): ", range(1, ROWS + 1)) - 1
            row_to_add = get_int_input("Row B to add: ", range(1, ROWS + 1)) - 1
            factor = save_input("Factor to multiply on row B before adding: ")

            row_copy = matrix[row_to_add][:COLUMNS]
            print("\nMultiply row:")
            for i, value in enumerate(row_copy):
                result = save_input("Column %i: %s * %s = " % (i + 1, math_expr(value), math_expr(factor)))
                row_copy[i] = result

            print("\nAdd rows:")
            for i, (target_value, add_value) in enumerate(zip(matrix[target_row][:COLUMNS], row_copy)):
                result = save_input("Column %i: %s + %s = " % (i + 1, math_expr(target_value), math_expr(add_value)))
                matrix[target_row][i] = result

            for i, value in enumerate(matrix[target_row][COLUMNS + 1:]):
                result = save_input("Result of %s + %s * %s = " % (math_expr(value), math_expr(factor), math_expr(matrix[row_to_add][COLUMNS + i + 1])))
                matrix[target_row][COLUMNS + i + 1] = result

            args = (target_row + 1, factor, row_to_add + 1)

        else:
            continue

    except KeyboardInterrupt:
        if save_input("\nOperation canceled. Quit programm? [y]es/[N]o: ").lower() == "y":
            break
        continue

    history.append((ACTION_MAP[action[0]], mat_copy(matrix), args))

print_history(history)

