from binance.client import Client
from src.util import MarketUtilities
import pymongo
from src.stream import BinanceStream
import time
from multiprocessing import Process


class CryptoLambda(object):
    key = "SdAlaaAOVAwlZM3po7txuWH15BE1hWHj1obQWVumK3bijpERellqiEYuRjLqSJm3"
    secret = "cuf8VV1nwjKCcz2v6nfQIz2d7jLrdyJ7XGMwoXljRrwL6nL1HLKlP6KhiD6xJRIg"

    def __init__(self):
        self.client = Client(self.key, self.secret)
        self.mongo_client = pymongo.MongoClient('localhost', 27017)
        self.db = self.mongo_client["ctr_storage"]
        self.stream = BinanceStream(self.client)
        self.stream.update_crypto_data(self.db)

    def run(self):
        start_time = time.time()
        while True:
            self.stream.update_crypto_data(self.db)
            time.sleep(1)
            market_opportunity = self.field_check()
            if market_opportunity is not None:
                print("Market Opportunity Found")
                print("Following Opp, Splitting Process")
                p = Process(target=MarketUtilities.follow_opp, args=(market_opportunity))
                p.start()

    def field_check(self):
        return {}








