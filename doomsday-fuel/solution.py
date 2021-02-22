from fractions import Fraction
from functools import reduce


def greatest_common_denominator(x, y):  # using Euclid's algorithm
    if x > y:
        x, y = y, x
    if y % x == 0:
        return x
    else:
        return greatest_common_denominator(y - x, x)


def lowest_common_multiple(x, y):
    return int(x * y / greatest_common_denominator(x, y))


def multiply_matrices(x, y):
    result = [[0] * len(y[0]) for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                result[i][j] += x[i][k] * y[k][j]
    return result


def find_terminal_states(m):
    terminal_states, non_terminal_states = {}, {}
    terminal_state_no, non_terminal_state_no = 0, 0
    for i in range(len(m)):
        total = sum(m[i])
        if total == m[i][i]:  # check if terminal state
            terminal_states[i] = terminal_state_no, 1
            terminal_state_no += 1
        else:
            non_terminal_states[i] = non_terminal_state_no, total
            non_terminal_state_no += 1
    return terminal_states, non_terminal_states


def multiply_row(val, row):
    return [val * i for i in row]


def sub_row(row_x, row_y):
    return [row_x[i] - row_y[i] for i in range(len(row_x))]


def get_inverse(matrix):  # using the Gauss-Jordan method
    n = len(matrix)
    inv_matrix = get_i_matrix(n)
    for i in range(n):
        inv_val = matrix[i][i] ** -1
        matrix[i] = multiply_row(inv_val, matrix[i])
        inv_matrix[i] = multiply_row(inv_val, inv_matrix[i])
        for j in range(0, i) + range(i + 1, n):
            val = matrix[j][i]
            matrix[j] = sub_row(matrix[j], multiply_row(val, matrix[i]))
            inv_matrix[j] = sub_row(inv_matrix[j], multiply_row(val, inv_matrix[i]))
    return inv_matrix


def get_q(m, non_terminal_states):
    return get_sub_standard_matrix(m, non_terminal_states, non_terminal_states)


def get_r(m, terminal_states, non_terminal_states):
    return get_sub_standard_matrix(m, non_terminal_states, terminal_states)


def sub_matrix_from_i(matrix):
    n = len(matrix)
    i_matrix = get_i_matrix(n)
    return [[i_matrix[i][j] - matrix[i][j] for j in range(n)] for i in range(n)]


def get_i_matrix(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def get_sub_standard_matrix(m, from_states, to_states):
    num_to_states = len(to_states)
    num_from_states = len(from_states)
    matrix = [[None] * num_to_states for _ in range(num_from_states)]
    for from_state in from_states.keys():
        for to_state in to_states.keys():
            from_matrix_index, total = from_states[from_state]
            to_matrix_index, _ = to_states[to_state]
            fraction = Fraction(m[from_state][to_state], total)
            matrix[from_matrix_index][to_matrix_index] = fraction
    return matrix


def format_output(probabilities):
    denominators = map(lambda fraction: fraction.denominator, probabilities)
    lcd = reduce(lowest_common_multiple, denominators)
    output = [x.numerator * lcd // x.denominator for x in probabilities] + [lcd]
    return output


def solution(m):  # solved using absorbing markov chain
    terminal_states, non_terminal_states = find_terminal_states(m)
    if 0 in terminal_states:
        return format_output([Fraction(1, 1)] + [Fraction(0, 1)] * (len(terminal_states) - 1))
    q = get_q(m, non_terminal_states)
    r = get_r(m, terminal_states, non_terminal_states)
    f = get_inverse(sub_matrix_from_i(q))
    fr = multiply_matrices(f, r)
    probabilities = fr[0]
    return format_output(probabilities)


print(solution([[0, 2, 1, 0, 0],
                [0, 0, 0, 3, 4],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]))
# [7, 6, 8, 21]

print(solution([[0, 1, 0, 0, 0, 1],
                [4, 0, 0, 3, 2, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]]))
# [0, 3, 2, 9, 14]
