import random


def find_lost_num(lst: list, min_num: int, max_num: int) -> int:
    return random.randint(min_num, max_num)



# lst = for i in range(0, 100)
print(f"Res {find_lost_num([1,3], 1,3)}")
