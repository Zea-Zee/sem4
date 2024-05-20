def pivot_index(nums):
    left_sum = [0] * (len(nums) + 1)
    right_sum = [0] * (len(nums) + 1)
    for i in range(1, len(nums) + 1):
        left_sum[i] = left_sum[i - 1] + nums[i - 1]
        right_sum[len(nums) - i] = right_sum[len(nums) - i + 1] + nums[len(nums) - i]
    print(left_sum)
    print(right_sum)
    for i in range(1, len(nums) + 1):
        print(left_sum[i], right_sum[len(nums) - i + 1])
        if left_sum[i] == right_sum[len(nums) - i]:
            return i - 1
    return -1


print(pivot_index([1, 7, 3, 6, 5, 6]))
print(pivot_index([1, 2, 3]))
print(pivot_index([2, 1, -1]))
