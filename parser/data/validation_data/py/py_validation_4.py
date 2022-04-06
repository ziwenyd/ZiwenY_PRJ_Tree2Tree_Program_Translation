def convertToTitle(columnNumber):
    array = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    result = ''
    if columnNumber <=26:
        result = array[columnNumber%26]
        return result
    else:
        while columnNumber > 0:
            remainder = columnNumber%26
            result =  array[remainder] + result 
            columnNumber = math.floor((columnNumber - 1) / 26)
    return result


