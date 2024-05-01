lists = [[1, 2, 4], [1, 4, 2], [2, 1, 4], [2, 4, 1], [4, 1, 2], [4, 2, 1]]

unique_lists = []
for lst in lists:
    if lst not in unique_lists:
        unique_lists.append(lst)

print(unique_lists)
