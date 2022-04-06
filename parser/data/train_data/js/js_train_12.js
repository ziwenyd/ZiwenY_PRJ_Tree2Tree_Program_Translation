function plusOne(digits) {
    let lastInteger = digits[digits.length-1]
    
    if (lastInteger < 9){
        digits[digits.length-1]++
    }
    else {
       let pointer = digits.length-1
       while (digits[pointer] == 9) {
           digits[pointer] = 0
           pointer--
       }
        if (pointer>=0){
            digits[pointer]++
        }
        else{
            digits.unshift(1)
        }
    }
       return digits
   };