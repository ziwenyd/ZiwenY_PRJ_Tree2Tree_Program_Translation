def isAnagram(s,t):
    if len(s) != len(t):
        return False
    map = {}
    count = 0
    for ch in s:
        if ch in map:
            count = map[ch]
            count +=1
        else:
            count = 1
        map[ch] = count
    for j in t:
        if j in map and map[j]:
            count = map[j]
            map[j] = count -1
        else:
            return False
    return True


