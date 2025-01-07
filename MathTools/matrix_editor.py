
OPERATORS = "+-*/^()"

def print_mat(mat, space=4):
    column_entry_length = 0
    for row in mat:
        column_entry_length = max(column_entry_length, len(max(row, key=len)))

    column_entry_length += space
    column_entry_length -= column_entry_length % space

    for i, row in enumerate(mat):
        print(i + 1, "", end="")
        if i == 0:
            print("┌ ", end="")
        elif i == len(mat) - 1:
            print("└ ", end="")
        else:
            print("│ ", end="")

        for j, value in enumerate(row):
            padding = "" if j == len(row) - 1 else " " * (column_entry_length - len(value))
            print(value + padding, end="")

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

def mat_copy(m):
    return [x[:] for x in m]

def math_expr(s):
    for op in OPERATORS:
        if op in s:
            return "(" + s + ")"
    return s

ROWS = int(input("Rows: "))
COLUMNS = int(input("Columns: "))

longest_value_length = 0

matrix = [[""] * COLUMNS for _ in range(ROWS)] 

for r in range(ROWS):
    for c in range(COLUMNS):
        value = ""
        while not value:
            value = input("Entry at %sr %sc: " % (r + 1, c + 1))
        matrix[r][c] = value

print("\nEntered matrix:")
print_mat(matrix)
print("\n")

for i, row in enumerate(matrix):
    perm_ext = ["0"] * ROWS
    perm_ext[i] = "1"
    row += ["|"] + perm_ext

swap_mapping_rows = {x: x for x in range(0, ROWS)}
history = [("start", mat_copy(matrix))]
ACTION_MAP = {
    "s": "swap rows",
    "~": "swap rows",
    "+": "add",
    "a": "add",
    "-": "subtract",
    "w": "Add with factor",
    "m": "Multiply",
    "e": "Edit value",
    "c": "swap columns",
}
while True:
    print_mat(matrix)
    action = input("[S]wap/Swap [c]olumn/[A]dd/Subtract[-]/Add [w]ith factor/[M]ultiply/[E]dit value/[Q]uit: ").lower()
    if not action:
        continue
    try:
        if action[0] == "q":
            if input("You sure to quit? [y]es/[N]o: ").lower() == "y":
                break
            continue

        elif action[0] == "e":
            print("NOTE: This operation can break the data validation (assuming you have no mistakes in your calculations so far... hehe")
            row = get_int_input("Row: ", range(1, ROWS + 1)) - 1
            column = get_int_input("Column: ", range(1, 2 * COLUMNS + 1)) - 1
            value = input("Enter value: ")
            matrix[row][column] = value

        elif action[0] in "s~":
            r1 = get_int_input("Row A to swap: ", range(1, ROWS + 1)) - 1
            r2 = get_int_input("Row B to swap: ", range(1, ROWS + 1)) - 1
            matrix[r1], matrix[r2] = matrix[r2], matrix[r1]
            swap_mapping_rows[r1] = r2
            swap_mapping_rows[r2] = r1

        elif action[0] == "c":
            c1 = get_int_input("Column A to swap: ", range(1, COLUMNS + 1)) - 1
            c2 = get_int_input("Column B to swap: ", range(1, COLUMNS + 1)) - 1

            for row in matrix:
                row[c1], row[c2] = row[c2], row[c1]

            print("NOTE: The result vector has to be changed in the according rows")

        elif action[0] in "m*":
            row = get_int_input("Row to multiply with a factor: ", range(1, ROWS + 1)) - 1
            factor = input("Factor to multiply with: ")

            for i, value in enumerate(matrix[row][:COLUMNS]):
                result = input("Column %i: %s * %s = " % (i + 1, math_expr(value), math_expr(factor)))
                matrix[row][i] = result

            original_row = swap_mapping_rows[row]
            row_change = input("Result of %s * %s = " % (math_expr(matrix[row][COLUMNS + original_row + 1]), math_expr(factor)))
            matrix[row][COLUMNS + original_row + 1] = row_change

        elif action[0] in "a+-":
            sign = "+" if action[0] in "a+" else "-"
            verb = "add" if action[0] in "a+" else "subtract (b in a-b)"
            target_row = get_int_input("Target row (which will be changed): ", range(1, ROWS + 1)) - 1
            row_to_add = get_int_input("Row to %s: " % verb, range(1, ROWS + 1)) - 1

            for i, (target_value, add_value) in enumerate(zip(matrix[target_row][:COLUMNS], matrix[row_to_add][:COLUMNS])):
                result = input("Column %i: %s %s %s = " % (i + 1, math_expr(target_value), sign, math_expr(add_value)))
                matrix[target_row][i] = result
            
            original_add_row = swap_mapping_rows[row_to_add]
            current_value_of_to_add_row = matrix[row_to_add][COLUMNS + original_add_row + 1]
            result = input("Result of %s %s %s = " % (math_expr(matrix[target_row][COLUMNS + original_add_row + 1]), sign, math_expr(current_value_of_to_add_row)))
            matrix[target_row][COLUMNS + original_add_row + 1] = result

        elif action[0] == "w":
            target_row = get_int_input("Target row A (which will be changed): ", range(1, ROWS + 1)) - 1
            row_to_add = get_int_input("Row B to add: ", range(1, ROWS + 1)) - 1
            factor = input("Factor to multiply on row B before adding: ")

            row_copy = matrix[row_to_add][:COLUMNS]
            print("\nMultiply row:")
            for i, value in enumerate(row_copy):
                result = input("Column %i: %s * %s = " % (i + 1, math_expr(value), math_expr(factor)))
                row_copy[i] = result

            print("\nAdd rows:")
            for i, (target_value, add_value) in enumerate(zip(matrix[target_row][:COLUMNS], row_copy)):
                result = input("Column %i: %s + %s = " % (i + 1, math_expr(target_value), math_expr(add_value)))
                matrix[target_row][i] = result

            original_add_row = swap_mapping_rows[row_to_add]
            current_value_of_to_add_row = matrix[row_to_add][COLUMNS + original_add_row + 1]
            result = input("Result of %s + %s * %s = " % (math_expr(matrix[target_row][COLUMNS + original_add_row + 1]), math_expr(factor), math_expr(current_value_of_to_add_row)))
            matrix[target_row][COLUMNS + original_add_row + 1] = result

        else:
            continue

    except KeyboardInterrupt:
        if input("\nOperation canceled. Quit programm? [y]es/[N]o: ").lower() == "y":
            break
        continue

    history.append((ACTION_MAP[action[0]], mat_copy(matrix)))
    print("\n\n")


print("\n\nHistory:")
for action, mat in history:
    print("Action:", action)
    print_mat(mat)
    print()
