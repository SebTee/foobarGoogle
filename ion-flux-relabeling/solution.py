def no_elements_in_perf_bin_tree(height):
    return (2 ** height) - 1


def get_children_values(value, height):
    right = value - 1
    left = value - no_elements_in_perf_bin_tree(height - 1) - 1
    return left, right


def get_parent(value_to_find, current_value, height, parent_value=-1):
    left, right = get_children_values(current_value, height)
    if value_to_find == current_value:
        return parent_value
    elif value_to_find > left:
        return get_parent(value_to_find, right, height - 1, current_value)
    else:
        return get_parent(value_to_find, left, height - 1, current_value)


def solution(h, q):
    p = []
    for i in q:
        p.append(get_parent(i, no_elements_in_perf_bin_tree(h), h))
    return p


print(solution(3, [7, 3, 5, 1]))
# -1,7,6,3

print(solution(5, [19, 14, 28]))
# 21,15,29
