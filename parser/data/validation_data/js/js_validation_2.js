var maxProfit = function(prices) {
    let totalProfit = 0;
    let maxPrice = prices[prices.length - 1];

    for(let i  = prices.length - 1; i >= 0; i--){
        if(prices[i] > maxPrice){
            maxPrice = prices[i];
        }
        if(maxPrice - prices[i] > totalProfit){
            totalProfit = maxPrice - prices[i];
        }
    }
    return totalProfit;
    
};