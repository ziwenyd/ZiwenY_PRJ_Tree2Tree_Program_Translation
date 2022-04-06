def merge(nums1, m, nums2, n):
    nums1_ptr = m - 1
    nums2_ptr = n - 1
    insert_ptr = m + n - 1

    while nums1_ptr >= 0 and nums2_ptr >= 0 :
        if nums1[nums1_ptr] > nums2[nums2_ptr]:
            nums1[insert_ptr] = nums1[nums1_ptr]
            insert_ptr-=1
            nums1_ptr-=1
        else:
            nums1[insert_ptr] = nums2[nums2_ptr]
            insert_ptr -=1
            nums2_ptr -=1        

    while nums2_ptr >= 0:
        nums1[insert_ptr] = nums2[nums2_ptr]
        insert_ptr-=1
        nums2_ptr-=1
    


