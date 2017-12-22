import pymongo
from pymongo import errors


class BinanceStream(object):
    def __init__(self, client):
        self.client = client

    def update_crypto_data(self, db, ticker):
        """
        Initialize our mongo db with our crypto assets
        :return: Nothing
        """
        symbol = ticker["symbol"]
        price = float(ticker["price"])
        data_entry = db.crypto_data.find_one({'symbol': symbol})
        if data_entry is None or data_entry["prices"] is None:
            data = {
                "symbol": symbol,
                "prices": [price]
            }
            try:
                result = db.crypto_data.insert_one(data)
                # print('One post: {0}'.format(result))
            except errors.ConnectionFailure:
                print("Couldn't Insert")
        else:
            prev_data = db.crypto_data.find_one({'symbol': symbol})
            prices = prev_data["prices"]
            db.crypto_data.update_one(
                {'symbol': symbol},
                {'$set': {"prices": prices.append(price)}}, upsert=False)

    def populate_database(self, db):
        for i in range(0, 60):
            for asset in self.client.get_all_tickers():
                symbol = asset["symbol"]
                price = float(asset["price"])
                data_entry = db.crypto_data.find_one({'symbol': symbol})
                # print(data_entry)
                if data_entry is None or data_entry["prices"] is None:
                    data = {
                        "symbol": symbol,
                        "prices": [price]
                    }
                    try:
                        result = db.crypto_data.insert_one(data)
                        # print('One post: {0}'.format(result))
                    except errors.ConnectionFailure:
                        print("Couldn't Insert")
                else:
                    prev_data = db.crypto_data.find_one({'symbol': symbol})
                    prices = prev_data["prices"]
                    result = db.crypto_data.update_one(
                        {'symbol': symbol},
                        {'$set': {"prices": prices.append(price)}}, upsert=False)
                    # print('One Update: {0}'.format(result))
