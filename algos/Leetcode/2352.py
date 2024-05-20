from collections import Counter


def equalPairs(grid: list[list[int]]) -> int:
    count = 0
    rows = {}

    for i in grid:
        row = tuple(i)
        rows[row] = 1 + rows.get(row, 0)

    for i in zip(*grid):
        count += rows.get(tuple(i), 0)

    return count


print(equalPairs([
    [3, 2, 1],
    [1, 7, 6],
    [2, 7, 7]
]))

# print(equalPairs([[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]))
