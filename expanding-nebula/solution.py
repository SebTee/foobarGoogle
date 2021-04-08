def f(neighbourhood):  # applying the rule to a neighbourhood and output the next iteration
    return sum(neighbourhood) == 1


def int_to_bool_list(x, no_bits):
    return [bool(x & (1 << n)) for n in range(no_bits)]


def bool_list_to_int(x):
    val = 0
    for i, bit in enumerate(x):
        val += (2 ** i) * int(bit)
    return val


def get_all_possible_columns(no_bits):
    for i in range(2 ** no_bits):
        yield int_to_bool_list(i, no_bits)


def get_column_in_g(g, i):
    return [g[j][i] for j in range(len(g))]


# get all possible next columns based on the previous preimage column and original column
def get_valid_columns(column, prev_column, prev_vals=None, i=0, saved_vals=None):
    for next_val in [True, False]:
        if prev_vals is None:
            for x in get_valid_columns(column, prev_column, [next_val], 0, {}):
                yield x
        else:
            if f(prev_column[i:i+2] + [prev_vals[i], next_val]) == column[i]:
                key = i, next_val
                if key in saved_vals:
                    for next_vals in saved_vals[key]:
                        yield prev_vals + next_vals
                else:
                    temp_saved_vals = []
                    if i < len(column) - 1:
                        for x in get_valid_columns(column, prev_column, prev_vals + [next_val], i + 1, saved_vals):
                            temp_saved_vals += [x[i+1:]]
                            yield x
                    else:
                        temp_saved_vals += [[next_val]]
                        yield prev_vals + [next_val]
                    saved_vals[key] = temp_saved_vals


# backtracking through columns since max column size is 10
def count_possible_preimages(g, prev_column, saved_results, column_no=0):
    count = 0
    row_len = len(g[0])
    for curr_column in get_valid_columns(get_column_in_g(g, column_no), prev_column):
        key = column_no, bool_list_to_int(curr_column)
        if key in saved_results:
            count += saved_results[key]
        else:
            new_count = 1
            if column_no < row_len - 1:
                new_count = count_possible_preimages(g, curr_column, saved_results, column_no + 1)
            saved_results[key] = new_count
            count += new_count
    return count


def solution(g):
    count = 0
    no_bits = len(g) + 1
    for i in get_all_possible_columns(no_bits):
        count += count_possible_preimages(g, i, {})
    return count


print(solution([[True, True, False, True, False, True, False, True, True, False],
                [True, True, False, False, False, False, True, True, True, False],
                [True, True, False, False, False, False, False, False, False, True],
                [False, True, False, False, False, False, True, True, False, False]]))
# 11567

print(solution([[True, False, True],
                [False, True, False],
                [True, False, True]]))
# 4

print(solution([[True, False, True, False, False, True, True, True],
                [True, False, True, False, False, False, True, False],
                [True, True, True, False, False, False, True, False],
                [True, False, True, False, False, False, True, False],
                [True, False, True, False, False, True, True, True]]))
# 254
