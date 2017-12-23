from src.market_watch import MarketWatch


if __name__ == '__main__':
    mw = MarketWatch(repopulate=False, period=.5)
    mw.run()
