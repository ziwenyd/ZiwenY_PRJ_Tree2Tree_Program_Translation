def maxSubArray(nums):
    result = float('-inf')
    sum = 0
    
    for num in nums:
        sum += num
        
        if sum > result:
            result = sum
        
        if sum < 0:
            sum = 0
    return result

    


