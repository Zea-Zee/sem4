def longestOnes(nums: list[int], k: int) -> int:
    if not nums:
        return 0
    cur = mx = l = 0
    flipped = 0
    for r in range(len(nums)):
        if nums[r] == 0:
            flipped += 1
        while flipped > k:
            if nums[l] == 0:
                flipped -= 1
            l += 1
        cur = r - l + 1
        mx = max(mx, cur)
    return mx

# Примеры использования:
print(longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2))  # Должно быть 6
print(longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3))  # Должно быть 10
print(longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2))  # Должно быть 6
