def isPalindrome(x):
    temp = x
    reversedNum = 0

    while temp >= 1:
        digit = math.floor(temp % 10)
        reversedNum = math.floor(reversedNum * 10 + digit)
        temp = math.floor(temp / 10)
    
    if x == reversedNum:
        return True
    
    return False


