function atomTest(){
    s = [1,2,3,4,5]
    a = 0
    for (let i=0; i < s.length; i++){
        if (s[i] < s[i+1]){
            a = s[i]
        }
        else{
            a = -1
        }
    }
    return a
}