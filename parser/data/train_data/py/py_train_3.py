def romanToInt(s):
    symbols = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }
    
    value = 0
    for i in range(0, len(s)):
        if i+1 >= len(s):
            value += symbols[s[i]]
        elif symbols[s[i]] < symbols[s[i+1]]:
            value -= symbols[s[i]]
        else:
            value += symbols[s[i]]
    
    return value


