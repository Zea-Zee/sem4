def maxProfit(prices, fee: int) -> int:
    #init with val < -10^4
    buy = -100_000
    sell = 0
    print(f"index:\t0\t1\t2\t3\t4\t5")
    print(f"price:\t1\t3\t2\t8\t4\t9")
    buy_history = []
    sell_history = []
    for price in prices:
        buy = max(buy, sell - price)
        buy_history.append(buy)
        sell = max(sell, buy + price - fee)
        sell_history.append(sell)

    print("buy  :", end='\t')
    print('\t'.join(str(x) for x in buy_history))

    print("sell :", end='\t')
    print('\t'.join(str(x) for x in sell_history))
    return sell

maxProfit([1,3,2,8,4,9], 2)
