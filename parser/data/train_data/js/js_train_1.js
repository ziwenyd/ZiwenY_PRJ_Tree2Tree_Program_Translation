function twoSum(nums, target){
    const map = new Map()
    for(let i=0; i<nums.length; i++){
        const complementary = target - nums[i]
        if(map.has(complementary)){
            return [i, map.get(complementary)]
        }
        map.set(nums[i], i)
    }
    return [-1, -1]
};
