function maxSubArray(nums) {
    let result = -Infinity
    let sum = 0
  
    for (num of nums) {
      sum += num
  
      if (sum > result) {
        result = sum
      }
  
      if (sum < 0) {
        sum = 0
      }
    }
    return result
};