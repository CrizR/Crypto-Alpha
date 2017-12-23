from binance.client import Client
from src.util import MarketUtilities
import pymongo
from src.stream import BinanceStream
import time
from multiprocessing import Process
from pymongo import errors
from src.notify import ClientNotif
import datetime


class MarketWatch(object):
    # secret: <your secret here>
    # key: <your key here>
    f = open("src/.authentication", "r")
    raw_file_data = f.readlines()
    file_info = {}
    for row in raw_file_data:
        split = row.split(":")
        file_info[split[0]] = split[1]

    key = file_info['key'].replace("\n", "")
    secret = file_info['secret'].replace("\n", "")
    twilio_sid = file_info["twilio_sid"].replace("\n", "")
    auth_token = file_info["auth_token"].replace("\n", "")

    def __init__(self, repopulate=False, period=1):
        """
        Initialize our market watch app with the given variables, creating a connection to the Binance API
        as well as creating a database to store price information
        :param repopulate: Whether or not we want to repopulate our database (will delete old database if true)
        :param period: The period to analyze the the prices over
        """
        self.client = Client(self.key, self.secret)
        self.period = period
        try:
            self.mongo_client = pymongo.MongoClient('localhost', 27017)
            print("Connected successfully")
        except pymongo.errors.ConnectionFailure:
            print("Connect Failed, Quitting")
            exit(1)
        self.db = self.mongo_client.crypto_data
        self.stream = BinanceStream(self.client)
        if repopulate:
            self.mongo_client.drop_database("crypto_data")
            self.stream.populate_database(self.db, self.period)
        self.notify = ClientNotif(self.twilio_sid,self.auth_token, self.mongo_client)

    def run(self):
        """
        Run the marketWatch
        :param period:
        :return:
        """
        start_time = time.time()
        while True:
            print(datetime.datetime.now())
            time.sleep(1)
            for asset in self.client.get_all_tickers():  # TODO:WE SHOULD ONLY STORE LAST 7 days of data
                self.stream.update_crypto_data(self.db, asset)
                market_opportunity = self.field_check(self.period)
                if market_opportunity is not None:
                    print("Market Opportunity Found")
                    # self.client.order_limit_buy()
                    # self.notify.message_all("Market Opportunity Found: " + market_opportunity["symbol"])
                    print("Following Opp, Splitting Process")
                    p = Process(target=self.follow_opp, args=(market_opportunity, self.period))
                    p.start()

    def field_check(self, asset):
        """
        Check to see if the given asset is a potential investment opportunity
        :param asset: The asset to check
        :return: The asset if it's worth looking into, or nothing if it's not
        """
        # Need to filter by volume
        # If the amount we own is greater than .1% [determine the right percent] of the volume, ignore
        asset = self.db.crypto_data.find_one({'symbol': asset['symbol']})
        if MarketUtilities.is_potential_opp(asset, self.period):
            return asset

    def follow_opp(self, asset, period):
        """
        While an opportunity exists on this asset, follow it closely
        :param asset: The asset and corresponding data
        :param period: The period to watch
        :return: Nothing
        """
        while True:
            time.sleep(1)
            if not MarketUtilities.is_potential_opp(asset, period):
                print("No Longer an Opportunity, Drop Asset")
                # self.notify.message_all("No Longer an Opportunity, Drop Asset: " + asset["symbol"])
                # self.client.order_limit_sell()
                exit(1)







