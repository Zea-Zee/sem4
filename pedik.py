import random


myset = set()
for i in range(1000_000):
    myset.add(random.randint(0, 1000))
for num, val in enumerate(myset):
    print(f"Car {num}: {val}")
