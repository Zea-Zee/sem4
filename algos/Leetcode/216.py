def combinationSum3(k: int, n: int):
    res = []
    digits = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    def backtrack(rem, digits, cur_sum, comb):
        # print(digits)
        if not rem and cur_sum == n:
            res.append(comb)
            for digit in comb:
                digits.remove(digit)
            return
        for digit in digits:
            digits_copy = digits.copy()
            digits_copy.remove(digit)
            backtrack(rem - 1, digits_copy, cur_sum + digit, comb + [digit])


    backtrack(k, digits, 0, [])
    return res


print(combinationSum3(3, 7))
