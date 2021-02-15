def get_primes():
    # prev_primes does not contain 2 since we step by 2
    prev_primes = []
    yield 2
    for potential_prime in range(3, 20232, 2):
        for potential_divisor in prev_primes:
            if potential_prime % potential_divisor == 0:
                break
        else:
            # runs if potential_prime isn't divisible by any of the prev_primes
            yield potential_prime
            prev_primes.append(potential_prime)


def get_primes_sub_str(start, length):
    end = start + length
    primes_string = ""
    primes = get_primes()
    while len(primes_string) < end:
        primes_string += str(primes.next())
    return primes_string[start: end]


def solution(x):
    return get_primes_sub_str(x, 5)


print(solution(0))
# 23571

print(solution(3))
# 71113
