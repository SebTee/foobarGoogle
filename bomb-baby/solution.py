def get_min_cycles(m, f):
    min_cycles = "impossible"
    minimum_val = min(m, f)
    maximum_val = max(m, f)
    cycles = maximum_val // minimum_val
    m, f = minimum_val, maximum_val % minimum_val
    while m > 1 and f > 1:
        minimum_val = min(m, f)
        diff = abs(m - f)
        m, f = minimum_val, diff
        cycles += 1
    if m == 1:
        min_cycles = cycles + f - 1
    elif f == 1:
        min_cycles = cycles + m - 1
    return min_cycles


def solution(m, f):
    return str(get_min_cycles(int(m), int(f)))


print(solution('4', '7'))
# 4

print(solution('2', '1'))
# 1

print(solution('3', '1'))
# impossible
