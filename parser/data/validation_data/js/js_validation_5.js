var containsNearbyDuplicate = function(nums, k) {
    num_set = new Set()
    
    for (let i=0; i < nums.length; i++) {
        if (num_set.has(nums[i])){
            return true
        }
        
        num_set.add(nums[i])
        if (num_set.size > k) {
            num_set.delete(nums[i - k])
        }
    }
    return false
}