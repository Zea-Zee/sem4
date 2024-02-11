def correlation_solution(x, y):
    avg_x = sum(x) / len(x)
    avg_y = sum(y) / len(y)
    return = sum((val_x - avg_x) * (val_y - avg_y) for val_x, val_y in zip(x, y))



correlation_solution([1, 2, 3], [4, 5, 6])
