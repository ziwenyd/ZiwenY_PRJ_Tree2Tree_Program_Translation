function strStr(haystack, needle) {
    hlen = haystack.length;
    nlen = needle.length;
    if(hlen===0 && nlen===0){
        return 0
    }
    if(hlen===0){
        return -1
    }
    diff = hlen - nlen + 1
    for(var i=0; i<hlen; i++){
        for(var j=i;j<diff;j++){
            if(haystack.substring(j, j+nlen)===needle){
                return j
            }
        }
        return -1
    }
};