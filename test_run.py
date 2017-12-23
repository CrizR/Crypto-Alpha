from src.market_watch import MarketWatch


if __name__ == '__main__':
    mw = MarketWatch(repopulate=True, period=.5)
    mw.run()
    # print(mw.retrieve_previous_opps())