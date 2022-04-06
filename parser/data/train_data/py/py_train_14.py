def climbStairs(n):
    arr = [1,1]
    for i in range(n-1):
        arr.append(None)
        
    for i in range(2, len(arr)):
        arr[i] = arr[i-1]+arr[i-2]
        
    idx = len(arr) -1
    
    return arr[idx]


