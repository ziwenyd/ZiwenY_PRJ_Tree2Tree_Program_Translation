def mySqrt(x):
    leftPointer = 1
    rightPointer = leftPointer * 2

    while rightPointer * rightPointer <= x:
        leftPointer = rightPointer
        rightPointer = leftPointer * 2
    
    while leftPointer < rightPointer:
        mid = leftPointer + math.floor((rightPointer - leftPointer) / 2)
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            leftPointer = mid + 1
        else:
            rightPointer = mid
        
    return leftPointer - 1


