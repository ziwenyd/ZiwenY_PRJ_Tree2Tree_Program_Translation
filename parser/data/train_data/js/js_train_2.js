function isPalindrome(x) {
    let temp = x
    let reversedNum = 0
    
    while (temp >= 1) {
        let digit = Math.floor(temp % 10)
        reversedNum = Math.floor(reversedNum * 10 + digit)
        temp = Math.floor(temp / 10)
    }
    
    if (x === reversedNum) {
        return true
    }
    return false
}