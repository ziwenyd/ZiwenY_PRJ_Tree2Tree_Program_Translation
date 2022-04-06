function removeDuplicates(nums) {
    let i = 0
    for (let j = 0; j < nums.length; j++) {
        if (nums[j] != nums[i]){
            i += 1
            nums[i] = nums[j]
        }
    }
    i += 1
    return i
};