def countBits(n: int) -> int:
    answer = [0] * (n + 1)
    for i in range(n + 1):
        answer[i] = answer[i >> 1] + (i & 1)

    return answer


print(countBits(5))
