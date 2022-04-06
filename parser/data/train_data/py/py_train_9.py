def searchInsert(nums, target):
    l = 0
    r = len(nums) -1

    if(nums[r] < target):
        return len(nums)

    while l <= r:
        mid = math.floor(l+(r-l)/2)
        if nums[mid]==target:
            return mid
        elif nums[mid]<target:
            l = mid+1;
        elif nums[mid]>target:
            r = mid-1;
    return r+1


