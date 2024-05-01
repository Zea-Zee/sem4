from collections import defaultdict, deque


def nearestExit(maze, entrance) -> int:
    # build graph
    n, m = len(maze), len(maze[0])
    graph = defaultdict(set)
    exits = set()
    for i in range(n - 1):
        for j in range(m - 1):
            if maze[i][j] == '.':
                if maze[i + 1][j] == '.':
                    graph[i * m + j].add((i + 1) * m + j)
                    graph[(i + 1) * m + j].add(i * m + j)
                if maze[i][j + 1] == '.':
                    graph[i * m + j].add(i * m + j + 1)
                    graph[i * m + j + 1].add(i * m + j)

    for i in [0, n - 1]:
        for j in range(m):
            if maze[i][j] == '.':
                exits.add([i * m + j])

    for i in range(n):
        for j in [0, m - 1]:
            if maze[i][j] == '.':
                exits.add([i * m + j])


    visited = set()
    q = deque([entrance[0] * m + entrance[1]])
    max_len = 0

    while q:
        v = q.popleft()
        visited.add(v)
        max_len += 1
        for u in graph[v]:
            if u not in visited:
                if u in exits:
                    return max_len
                q.append(u)

    return -1



print(nearestExit(maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]))
