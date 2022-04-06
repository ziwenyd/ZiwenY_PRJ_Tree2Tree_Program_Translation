var getRow = function (rowIndex) {
    const res = []
    
    for (let i = 0; i<rowIndex+1; i++){
        res.push(null)
    }
      
    let currentVal = 1;
    res[0] = currentVal;
    res[res.length - 1] = 1;
    let i = 1
    while(i <= rowIndex /2){
        currentVal *= rowIndex - i + 1;
        currentVal /= i;

        let left = i;
        let right = res.length - i - 1;
        if (left !== right) {
            res[res.length - i - 1] = currentVal;
        }
        res[i] = currentVal;
        i ++
    }
    return res;
  };