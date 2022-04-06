def removeElement(nums, val):
    zeroStartIdx = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[zeroStartIdx] = nums[i]
            zeroStartIdx += 1
    return zeroStartIdx


