import pymongo
from pymongo import errors


class BinanceStream(object):
    def __init__(self, client):
        self.client = client

    def update_crypto_data(self, db):
        """
        Initialize our mongo db with our crypto assets
        :return: Nothing
        """
        for ticker in self.client.get_all_tickers():  # WE SHOULD ONLY STORE LAST 7 days of data
            if db.find({'symbol': ticker['symbol']}) is None:
                data = {
                    "symbol": ticker["symbol"],
                    "prices": [ticker["price"]]
                }
                try:
                    result = db.insert(data)
                    print('One post: {0}'.format(result.inserted_id))
                except errors.ConnectionFailure:
                    print("Couldn't Connect")
            else:
                prev_data = db.find({'symbol', ticker['symbol']})
                db.update_one(
                    {'symbol': ticker["symbol"]},
                    {'$set':{"prices": prev_data["prices"].append(ticker['price'])}},
                    upsert=False)
