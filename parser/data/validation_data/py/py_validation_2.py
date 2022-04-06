def maxProfit(prices):
    totalProfit = 0
    maxPrice = prices[len(prices) - 1]
    
    for i in range(len(prices)-1, -1, -1):
        if prices[i] > maxPrice:
            maxPrice = prices[i]
        
        if maxPrice - prices[i] > totalProfit:
            totalProfit = maxPrice - prices[i]
        
    return totalProfit


