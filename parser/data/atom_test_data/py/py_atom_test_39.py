def atomTest():
    s = [1,2,3,4,5]
    a = 0
    for i in range(0, len(s)):
        if i+1 >= len(s):
            a = -1
        if s[i] < s[i+1]:
            a = s[i]
        else:
            a = -1
    return a


