def isValid(s):
    openB = ['(', '{', '[']
    closeB = [')','}',']']
    stack  = []

    for c in s:
        if c in openB:
            x = openB.index(c)
            stack.append(openB.index(c))
        elif len(stack) == 0:
            return False
        elif closeB.index(c) != stack.pop():
            return False
        else:
            pass
    if len(stack) == 0:
        return True
    return False


