SECONDS_PER_HOUR = 3600

class MarketUtilities(object):
    """
    Used to abstract out Market Utility functions for determining certain trends or executing certain actions dependent
    upon those trends
    """

    @staticmethod
    def get_stability_ratio(data, period):
        """
        Return difference between high and low range over the avg price of the period
        :return: The ratio
        """
        period_stats = MarketUtilities.get_period_data(data, period)["stats"]
        diff = (period_stats["high"] - period_stats["low"])
        if diff == 0:
            return 0
        return (period_stats["high"] - period_stats["low"]) / period_stats["avg"]

    @staticmethod
    def get_period_data(data, period):
        """
         We store a price per second so to get the period of prices where period is in hours
         We store the last period * 3600 values
        :param data: The data to analyze
        :param period: The period to look at
        :return: The stats and data associated with the data over the given period
        """
        i = 0
        period_stats = {
            "high": -1,
            "low": 99999999,
            "sum": 0,
            "avg": 0
        }
        period_data = []
        for price in data:
            if i >= len(data) - period * SECONDS_PER_HOUR:
                if price > period_stats["high"]:
                    period_stats["high"] = price

                if price < period_stats["low"]:
                    period_stats["low"] = price
                period_stats["sum"] += price
                period_data.append(price)
            i += 1
        if period * SECONDS_PER_HOUR > len(data):
            size = len(data)
        else:
            size = period * SECONDS_PER_HOUR
        period_stats["avg"] = period_stats["sum"] / size
        return {"stats": period_stats, "data": period_data}

    @staticmethod
    def get_percent_increase(data, period):
        """
        Determine the momentum positive or negative that the data has over the period
        :param data: The data to analyze
        :param period: The period to look at
        :return: The momentum of the data during this period
        """
        price_data = MarketUtilities.get_period_data(data, period)["data"]
        starting_value = price_data.pop(0)
        end_value = price_data.pop()
        return ((end_value - starting_value) / starting_value) * 100

    @staticmethod
    def get_exponential_moving_average(data, period):
        """
        Determine the ema of the asset over the given period
        :param data: The data associated with the asset
        :param period: The period to look at
        :return: The ema
        """
        multiplier = (2 / period + 1)
        period_data = MarketUtilities.get_period_data(data, period)
        prev_period_data = MarketUtilities.get_period_data(data, period * 2)["data"][:int(len(period_data["data"]) / 2)]
        prev_sma = sum(prev_period_data) / period
        return (period_data["data"].pop() - prev_sma) * multiplier + prev_sma

    @staticmethod
    def is_flaggable(asset, period):
        """
        Determines whether or not the asset is potentially valuable
        :param asset: The asset to look at
        :param period: The period to watch
        :return: The boolean associated with the decision
        """
        if asset["prices"] is not None:
            stability_ratio = MarketUtilities.get_stability_ratio(asset["prices"], period)
            percent_increase = MarketUtilities.get_percent_increase(asset["prices"], period)
            fast_moving_avg = MarketUtilities.get_exponential_moving_average(asset["prices"], 720)
            slow_moving_avg = MarketUtilities.get_exponential_moving_average(asset["prices"], 1440)
            return stability_ratio < .01 and percent_increase > 5 and fast_moving_avg > slow_moving_avg
        else:
            return False