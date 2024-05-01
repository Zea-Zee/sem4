n, m = input().split()
n, m = int(n), int(m)
# print(n, m)

maxes = []
for mx in input().split():
    maxes.append(int(mx))

error_counter = 0
res = [[0] * (n + 1) for _ in range(m)]

for i in range(m):
    values = input().split()
    # print(f"values is {values}")
    for j in range(n + 1):
        val = values[j]
        if j == 0:
            res[i][j] = val
        elif val != '-':
            if int(val) > maxes[j - 1] or int(val) < 0:
                error_counter += 1
                res[i][j] = 'N'
            else:
                res[i][j] = 'Y'
        else:
            res[i][j] = 'Y'


# print(maxes)
print(error_counter)
# print(res)
for el in res:
    print(' '.join(el))
