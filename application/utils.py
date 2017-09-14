def get_price(results, symbol):
    stock_obj = [results[x] for x in range(len(results))
                 if (type(results[x]) is not None and
                 results[x]['symbol'] == symbol)][0]
    return (stock_obj['last_extended_hours_trade_price']
            if stock_obj['last_extended_hours_trade_price'] is not None
            else stock_obj['last_trade_price']
            if stock_obj['last_trade_price'] is not None
            else (stock_obj['ask_price'] + stock_obj['bid_price']) / 2)
