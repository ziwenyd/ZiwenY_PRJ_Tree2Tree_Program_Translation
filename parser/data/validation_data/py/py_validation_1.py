def getRow(rowIndex):
    res = []
    for i in range(rowIndex+1):
        res.append(None)
    
    currentVal = 1
    res[0] = currentVal
    res[len(res) - 1] = 1
    i = 1
    while i <= rowIndex//2:
        currentVal = currentVal *(rowIndex - i + 1)
        currentVal = currentVal // i
        left = i
        right = len(res) - i - 1
        if left != right:
            res[len(res) - i - 1] = currentVal

        res[i] = currentVal
        i +=1
    return res


