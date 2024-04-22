def containsNearbyAlmostDuplicate(
    nums: list[int], indexDiff: int, valueDiff: int
) -> bool:
    min_val = min(nums)
    get_bucket_key = lambda x: (x - min_val) // (valueDiff + 1)
    dct = collections.defaultdict(lambda: sys.maxsize)
    for i, num in enumerate(nums):
        key = get_bucket_key(num)
        for neighbour in [dct[key - 1], dct[key], dct[key + 1]]:
            if abs(num - neighbour) <= valueDiff:
                return True
        dct[key] = num
        if i >= k:
            dct.pop(get_bucket_key(nums[i - indexDiff]))
    return False


print(containsNearbyAlmostDuplicate([1, 2, 3, 1], 3, 0))
