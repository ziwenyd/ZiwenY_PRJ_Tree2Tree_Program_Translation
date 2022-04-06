function mySqrt(x) {
    let leftPointer = 1
    let rightPointer = leftPointer * 2
  
    while (rightPointer * rightPointer <= x) {
      leftPointer = rightPointer
      rightPointer = leftPointer * 2
    }
  
    while (leftPointer < rightPointer) {
      const mid = leftPointer + Math.floor((rightPointer - leftPointer) / 2)
      if (mid * mid === x) {
        return mid;
      } else if (mid * mid < x) {
        leftPointer = mid + 1
      } else {
        rightPointer = mid
      }
    }
    return leftPointer - 1
  };