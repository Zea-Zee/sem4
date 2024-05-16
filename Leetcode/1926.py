from collections import deque, defaultdict
from typing import List

class Solution:
    def nearestExit(self, maze: List[List[str]], entrance: List[int]) -> int:
        n, m = len(maze), len(maze[0])
        graph = defaultdict(set)
        exits = set()

        # Добавление рёбер в граф
        for i in range(n):
            for j in range(m):
                if maze[i][j] == '.':
                    if i > 0 and maze[i - 1][j] == '.':
                        graph[(i, j)].add((i - 1, j))
                        graph[(i - 1, j)].add((i, j))
                    if j > 0 and maze[i][j - 1] == '.':
                        graph[(i, j)].add((i, j - 1))
                        graph[(i, j - 1)].add((i, j))

        # Поиск всех выходов
        for i in [0, n - 1]:
            for j in range(m):
                if maze[i][j] == '.' and [i, j] != entrance:
                    exits.add((i, j))
        for i in range(0, n):
            for j in [0, m - 1]:
                if maze[i][j] == '.' and [i, j] != entrance:
                    exits.add((i, j))

        visited = set()
        q = deque([(entrance[0], entrance[1], 0)])  # Добавляем третий элемент для отслеживания длины пути

        while q:
            x, y, dist = q.popleft()
            visited.add((x, y))
            if (x, y) in exits and (x, y) != tuple(entrance):
                return dist
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == '.' and (nx, ny) not in visited:
                    q.append((nx, ny, dist + 1))
                    visited.add((nx, ny))  # Добавляем в посещённые здесь, чтобы избежать повторных посещений

        return -1

# Пример использования
solution = Solution()
maze = [["+",".","+","+","+","+","+"],["+",".","+",".",".",".","+"],["+",".","+",".","+",".","+"],["+",".",".",".",".",".","+"],["+","+","+","+",".","+","."]]
entrance = [0, 1]
print(solution.nearestExit(maze, entrance))  # Ожидаемый результат: 7
