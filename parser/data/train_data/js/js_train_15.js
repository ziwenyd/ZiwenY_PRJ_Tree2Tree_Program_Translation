function merge(nums1, m, nums2, n) {
    let nums1_ptr = m - 1;
    let nums2_ptr = n - 1;
    let insert_ptr = m + n - 1;
    
    while(nums1_ptr >= 0 && nums2_ptr >= 0 ){
        if(nums1[nums1_ptr] > nums2[nums2_ptr]){
            nums1[insert_ptr] = nums1[nums1_ptr];
            insert_ptr--;
            nums1_ptr--;
        }else{
            nums1[insert_ptr] = nums2[nums2_ptr];
            insert_ptr--;
            nums2_ptr--;
        }
    }
    
    while(nums2_ptr >= 0){
        nums1[insert_ptr] = nums2[nums2_ptr];
        insert_ptr--;
        nums2_ptr--;
    }
};