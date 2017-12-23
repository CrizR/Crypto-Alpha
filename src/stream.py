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
                "prices": [price],
                "following":False
            }
            try:
                result = db.crypto_data.insert_one(data)
                # print('One post: {0}'.format(result))
            except errors.ConnectionFailure:
                print("Couldn't Insert")
        else:
            prev_data = db.crypto_data.find_one({'symbol': symbol})
            prices = prev_data["prices"]
            prices.append(price)
            try:
                result = db.crypto_data.update_one(
                    {'symbol': symbol},
                    {'$set': {"prices": prices}}, upsert=False)
                # print('One Update: {0}'.format(result))
            except errors.ConnectionFailure:
                print("Couldn't Insert")

    def reset_watchlist(self, db):
        """
        Resets the boolean values of our watchlist to False
        :param db: The database to reset
        :return: Nothing
        """
        for asset in db.crypto_data.find():
            try:
                result = db.crypto_data.update_one(
                    {'symbol': asset["symbol"]},
                    {'$set': {"following": False}}, upsert=False)
            except errors.ConnectionFailure:
                print("Couldn't Update")

    def populate_database(self, db, period):
        for i in range(0, int(period * 3600)):
            for asset in self.client.get_all_tickers():
                symbol = asset["symbol"]
                price = float(asset["price"])
                data_entry = db.crypto_data.find_one({'symbol': symbol})
                if data_entry is None or data_entry["prices"] is None:
                    data = {
                        "symbol": symbol,
                        "prices": [price],
                        "following": False
                    }
                    try:
                        result = db.crypto_data.insert_one(data)
                        # print('One post: {0}'.format(result))
                    except errors.ConnectionFailure:
                        print("Couldn't Insert")
                else:
                    prev_data = db.crypto_data.find_one({'symbol': symbol})
                    prices = prev_data["prices"]
                    prices.append(price)
                    try:
                        result = db.crypto_data.update_one(
                            {'symbol': symbol},
                            {'$set': {"prices": prices}}, upsert=False)
                        # print('One Update: {0}'.format(result))
                    except errors.ConnectionFailure:
                        print("Couldn't Update")

