def lengthOfLastWord(s):
    index = len(s) - 1
    while index >= 0 and s[index] == ' ':
        index -= 1
    
    result = 0
    while index >= 0 and s[index] != ' ': 
        index -= 1
        result += 1
    
    return result


