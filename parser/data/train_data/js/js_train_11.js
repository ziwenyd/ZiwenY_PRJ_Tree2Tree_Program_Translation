function lengthOfLastWord(s) {
    let index = s.length - 1
    while (index >= 0 && s[index] === ' ') {
      index -= 1
    }
  
    let result = 0
    while (index >= 0 && s[index] !== ' ') {
      index -= 1
      result += 1
    }
  
    return result
  };