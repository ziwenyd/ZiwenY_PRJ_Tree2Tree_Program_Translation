def strStr(haystack, needle):
    hlen = len(haystack)
    nlen = len(needle)
    if hlen == 0 and nlen == 0:
        return 0
    if hlen == 0:
        return -1
        
    diff = hlen - nlen + 1
    for i in range(hlen):
        for j in range(diff):
            if haystack[j : j+nlen] == needle:
                return j
        return -1
    


