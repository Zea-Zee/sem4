def guess(g, n):
    if g > n:
        return -1
    if g < n:
        return 1
    return 0


def guessNumber(n: int) -> int:
    l = -1
    while l < n - 1:
        m = (l + n) // 2
        guess_res = guess(m, 6)
        if guess_res < 0:
            n = m
        elif guess_res > 0:
            l = m
        else:
            return n


guessNumber(10)
