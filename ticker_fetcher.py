import yfinance as yf


class TickerFetcher:
    """
    This class is responsible for fetching financial information about a specific ticker symbol using the yfinance library.

    It provides functionality to retrieve both current information and historical data for a given ticker symbol.
    This includes data such as the latest trading price, market capitalization, trading volume,
    and historical price movements over specified periods and interval
    """

    @staticmethod
    def fetch_ticker_info(ticker_symbol, period, interval):
        """
        Fetches and returns information and historical data for a given ticker symbol.

        The method retrieves general information about the ticker, such as its current trading price and other relevant
        details. It also fetches historical data for the ticker, which includes historical price movements over a
        specified time period and at a given interval.
        :param ticker_symbol: Ticker symbol of the searching company, or its name
        :param period: Period for which you need the historical data
        :param interval: Interval for which you need the historical data
        :return:
        """
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.fast_info
        historical_data = ticker.history(period=period, interval=interval)
        return info, historical_data
