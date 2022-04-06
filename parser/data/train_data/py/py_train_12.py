def plusOne(digits):
    lastInteger = digits[len(digits)-1]

    if lastInteger < 9:
        digits[len(digits) -1] += 1
    else:
        pointer = len(digits)-1
        while digits[pointer] == 9:
            digits[pointer] = 0
            pointer -=1
    
        if pointer>=0:
            digits[pointer] +=1
        else:
            digits.insert(0,1)
    return digits


