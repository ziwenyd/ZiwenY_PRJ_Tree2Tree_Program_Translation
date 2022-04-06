def singleNumber(nums):
    counts = {}
    output = None
    for num in nums:
        if num in counts:
            counts[num]  = counts[num] + 1
        else:
            counts[num] = 1
    for k in range(len(nums)):
        if counts[nums[k]] == 1:
            output = nums[k]
            break
    return output


