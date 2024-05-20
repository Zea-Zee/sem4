from bisect import bisect_left
from collections import defaultdict
from math import inf


def longestCommonSubsequence(text1: str, text2: str) -> int:
    dp = [[0 for _ in range(len(text2) + 1)] for _ in range(len(text1) + 1)]
    for i in range(1, len(text1) + 1):
        for j in range(1, len(text2) + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]



def fastLongestCommonSubsequence(text1: str, text2: str) -> int:
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    pos = defaultdict(list)

    #we define all characters used in text2 to save some bytes of memory
    used_chars = set(text2)

    for i, c in enumerate(text1):
        if c in used_chars:
            #so append only if this we'll see this charcle
            pos[c].append(i)

    #fill by max num cuz we'll find least value position to paste
    lcs = [inf] * len(text1)

    for c in text2:
        print(f"c: '{c}' pos[c]: {pos[c]}")
        for i in reversed(pos[c]):
            lcs[bisect_left(lcs, i)] = i
            print(f"    i: {i}lcs: {lcs}")

    return bisect_left(lcs, inf)


# print(longestCommonSubsequence('XMJYAUZ', 'MZJAWXU'))
# print(longestCommonSubsequence('ABCDE', 'ACE'))
# print(fastLongestCommonSubsequence('abcba', 'abcbcba'))
print(fastLongestCommonSubsequence('ACE', 'ABCDE'))

# pos = {'A': [0], 'C': [1], 'E': [2]}
# lcs = [inf, inf, inf, inf, inf]
# c = 'A', i = 0 lcs = [0, inf, inf, inf, inf]
# c = 'B', we'll skip due to there is no B in pos, so it just will create empty list
# c = 'C', i = 1 lcs = [0, 1, inf, inf, inf]
# c = 'D', we'll skip due to there is no B in pos, so it just will create empty list
# c = 'E', i = 2 lcs = [0, 1, 2, inf, inf]
# the most left inf is at 3rd pos, so there is 3 letters correct
