def isHappy(num):
    if num == 1:
        return True
    hash = set()
    while num !=1:
        current = num
        sum = 0
        while current !=0:
            sum += math.floor((current%10)*(current%10))
            current = math.floor(current/10)
        if sum in hash:
            return False
        hash.add(sum)
        num = sum
    return True
    


