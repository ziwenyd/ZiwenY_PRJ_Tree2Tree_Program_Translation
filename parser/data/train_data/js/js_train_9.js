function searchInsert(nums, target) {
    var l = 0;
    var r = nums.length-1;
    
    if(nums[r] < target){
        return nums.length
    } 
    while (l<=r){
       mid = Math.floor(l+(r-l)/2)
       if(nums[mid]==target){
           return mid
       }
       else if(nums[mid]<target){
           l = mid+1;
       }
       else if(nums[mid]>target){
           r = mid-1;
       }
        else{  
        } 
    }
    return r+1
};