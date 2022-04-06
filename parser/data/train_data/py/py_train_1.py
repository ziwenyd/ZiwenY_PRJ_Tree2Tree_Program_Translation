def twoSum(nums, target):
    map = {}
    for i in range(len(nums)):
        complementary = target - nums[i]
        if complementary in map:
            return [i, map.get(complementary)]
        map[nums[i]] = i
    return [-1, -1]


