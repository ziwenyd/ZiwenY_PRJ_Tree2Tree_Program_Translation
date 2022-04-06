function isValid(s) {
    openB = ["(","[","{"]
    closeB = [")","]","}"]
    stack = []

    for(c of s){
        if(openB.includes(c)){
            stack.push(openB.indexOf(c))
        }
        else if (stack.length === 0){
            return false
        }
        else if(closeB.indexOf(c) != stack.pop()){
            return false
        } 
        else{
        }
    }
    if(stack.length === 0) return true
    return false  
};
