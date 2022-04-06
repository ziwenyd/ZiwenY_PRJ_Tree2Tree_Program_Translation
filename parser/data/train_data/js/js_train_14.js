function climbStairs(n) {
    let arr = [1,1]
    for (let i = 0; i < n-1; i++){
        arr.push(null)
    }

    for (let i=2; i<arr.length; i++){
        arr[i] = arr[i-1]+arr[i-2]
    }
    let idx = arr.length-1
    return arr[idx]
};
