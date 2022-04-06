var singleNumber = function(nums) {
    const counts = {};
    let output = null
    for( num of nums){
        if (num in counts){
            counts[num]  = counts[num] + 1
        }
        else{
            counts[num] = 1
        }
    }
    
    for(let k=0; k<nums.length; k++){
        if(counts[nums[k]] === 1){
            output = nums[k];
            break;
        }
    }
    return output;
};