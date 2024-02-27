# подключаем модуль случайных чисел
import random
import time


def count_pi(n):
    start = time.time()
    i = 0
    count = 0
    while i < n:
        x = random.random()
        y = random.random()
        if (pow(x, 2) + pow(y, 2)) < 1:
            count += 1
        i += 1
    print(f"Estimated time: {time.time() - start} s")
    return 4 * (count / n)


print(count_pi(10000000))
print(count_pi(100000000))
print(count_pi(1000000000))
print(count_pi(1000000000))
