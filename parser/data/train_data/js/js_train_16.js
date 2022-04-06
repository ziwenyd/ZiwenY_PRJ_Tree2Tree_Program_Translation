function isHappy(num) {
    if(num==1){
          return true;
    }
    let hash = new Set();
    while(num!=1){
        let current=num;
        let sum =0;
        while(current!=0){
            sum+=Math.floor((current%10)*(current%10))
            current=Math.floor(current/10);
        }
        if(hash.has(sum)){
            return false;
        }
        hash.add(sum);
        num=sum;
    }
    return true;
  };