def longestCommonPrefix(strs):
    strs.sort()
    for i in range(0, len(strs[0])):
        if strs[0][i] != strs[len(strs) - 1][i]:
            return strs[0][0:i]
    
    return strs[0]


