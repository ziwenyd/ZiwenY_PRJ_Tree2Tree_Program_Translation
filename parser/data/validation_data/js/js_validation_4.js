var convertToTitle = function(columnNumber) {
    var array = ['Z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'];
    let result = '';
    if(columnNumber <= 26){
        result = array[columnNumber%26];
        return result;
    } else {
        
        while(columnNumber > 0){
            let remainder = columnNumber%26;
            result =  array[remainder] + result ;
            columnNumber = Math.floor((columnNumber - 1) / 26);
        }
    }
    return result;
};