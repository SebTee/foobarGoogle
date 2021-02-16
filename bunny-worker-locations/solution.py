def get_horizontal_id(n):
    return int(n * (n + 1) / 2)  # formula for triangular numbers


def get_vertical_id(n):
    return int(n * (n - 1) / 2) + 1


def solution(x, y):
    bunny_id = get_horizontal_id(x) + get_vertical_id(y + x - 1) - get_vertical_id(x)
    return str(bunny_id)


print(solution(5, 10))
# 96

print(solution(3, 2))
# 9
