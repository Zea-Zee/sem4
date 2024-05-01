from collections import Counter


def closeStrings(word1: str, word2: str) -> bool:
    a = Counter(word1).values()
    b = Counter(word2).values()
    print(a)
    print(b)
    return sorted([el for el in b]) == sorted([el for el in a])

    # print(a)
    # print(b.items())

    w1_set = set(word1)
    w2_set = set(word2)

    if w1_set != w2_set:
        return False

    w1_counts = [0] * len(w1_set)
    w2_counts = [0] * len(w2_set)

    i = 0
    for ch in w1_set:
        w1_counts[i] = word1.count(ch)
        i += 1

    i = 0
    for ch in w1_set:
        w2_counts[i] = word2.count(ch)
        i += 1

    return sorted(w1_counts) == sorted(w2_counts)


# closeStrings('abc', 'cba')
print(closeStrings('abbzccca', 'babzzczc'))
