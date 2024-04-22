def increasingTriplet(nums: list[int]) -> bool:
        sol = [float('inf'), float('inf'), float('inf')]
        for el in nums:
            if el <= sol[0]:
                sol[0] = el
            elif el <= sol[1]:
                sol[1] = el
            elif el <= sol[2]:
                sol[2] = el
                return True
        return False


print(increasingTriplet([1,2,3,4,5]))
print(increasingTriplet([5,4,3,2,1]))
print(increasingTriplet([2,1,5,0,4,6]))
