even = [
    '0', '2', '4', '6', '8'
]

odd = [
    '1', '3', '5', '7', '9'
]


# def find_multiples(n, k):
#     num = 10**(n-1) // k * k
#     end = 10**n

#     multiples = []
#     while num < end:
#         snum = str(num)
#         parity = True if snum[0] in even else False
#         for i in range(len(snum[1:]), -1, -1):
#             if (True if snum[i] in even else False) == parity:
#                 if snum[i] == '9':
#                     if i == 0:
#                         return multiples
#                     else:
#                         snum = snum[:i - 1] + str(int(snum[i - 1]) + 1) + '0' * (len(snum) - i - 2)


#             else:
#                 multiples.append(num)

#     return multiples

# n, k = map(int, input().split())
# # print(find_multiples(n, k))
# print(len(find_multiples(n, k)))
# # print(len(find_multiples(n, k)))



# def generate_numbers(n, k, current, is_even, count, MOD=10**9 + 7):
#     if len(current) == n:
#         number = int(current)
#         if number % k == 0:
#             return (count + 1) % MOD
#         return count

#     next_digits = even if not is_even else odd

#     for digit in next_digits:
#         count = generate_numbers(n, k, current + digit, not is_even, count, MOD)

#     return count


# def find_valid_multiples(n, k):
#     count = 0
#     for first_digit in odd:
#         count = generate_numbers(n, k, first_digit, False, count)
#     if n > 1:
#         for first_digit in even:
#             count = generate_numbers(n, k, first_digit, True, count)

#     return count

# n, k = map(int, input().split())
# print(find_valid_multiples(n, k))



# def generate_valid_multiples(n, k, MOD=10**9 + 7):
#     start = 10**(n-1)
#     if start % k != 0:
#         start += k - (start % k)
#     end = 10**n
#     count = 0

#     for num in range(start, end, k):
#         snum = str(num)
#         if len(snum) > n:
#             break

#         valid = True
#         for i in range(1, len(snum)):
#             if (snum[i-1] in even) == (snum[i] in even):
#                 valid = False
#                 break

#         if valid:
#             count = (count + 1) % MOD

#     return count

# n, k = map(int, input().split())
# print(generate_valid_multiples(n, k))

MOD = 10**9 + 7


def count_valid_numbers(n, k):
    dp_even = [[0 for _ in range(k)] for _ in range(n + 1)]
    dp_odd = [[0 for _ in range(k)] for _ in range(n + 1)]

    for digit in range(10):
        if not digit:
            continue
        remainder = digit % k
        if not digit % 2:
            dp_even[1][remainder] += 1
        else:
            dp_odd[1][remainder] += 1

    for i in range(2, n + 1):
        for j in range(k):
            for digit in range(10):
                new_remainder = (j * 10 + digit) % k
                if not digit % 2:
                    dp_even[i][new_remainder] += dp_odd[i - 1][j]
                else:
                    dp_odd[i][new_remainder] += dp_even[i - 1][j]


    return (dp_even[n][0] % MOD + dp_odd[n][0] % MOD) % MOD

n, k = map(int, input().split())
print(count_valid_numbers(n, k))
