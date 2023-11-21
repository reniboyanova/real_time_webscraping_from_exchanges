import json
from datetime import datetime

import pytz
import yfinance as yf
from forex_python.converter import CurrencyRates
# from colections_of_tickers import CollectionsOfTickers as ct
from ticker_storage import TickerStorage as ts
from helprers import convert_to_utc_time, prompt_user_to_paste_period_interval


class FetchData:
    """
    The FetchData class retrieves information about financial tickers.

    It fetches information for a given ticker or company name, including the last price,
    currency, exchange, and timezone. It also provides historical data for the ticker
    over a specified period and interval.
     Class uses 'yfinance' library

    Attributes:
        ticker_to_search (str): The ticker symbol or company name to search for.
        __library_with_tickers (dict): A library of tickers grouped by company.
        __collected_info (dict): Collected information for each ticker.
        __tickers_list (list): List of tickers associated with the searched company.

    """

    def __init__(self, ticker_to_search):
        self.ticker_to_search = ticker_to_search.upper()
        self.__library_with_tickers = ts().collection_stock_tickers
        self.__collected_info = {}
        self.__tickers_list = []

    def __get_tickers_by_company(self):
        """
        Finds and sets the tickers associated with the searched company.

        Checks if the provided ticker or company name exists in the ticker library and,
        if so, sets these tickers to __tickers_list.

        Raises:
        ValueError: If the ticker or company name is not found.
        :return:
        """
        for company, tickers in self.__library_with_tickers.items():
            if self.ticker_to_search in tickers or self.ticker_to_search in company:
                self.__tickers_list = tickers
                return
        raise ValueError(f"Ticker '{self.ticker_to_search}' not found in any company.")

    def __fetch_tickers_info(self, period, interval):
        """
        Retrieves and collects information for each ticker in the ticker list.
        :param period: Takes period by user (it cans be in some drop-down menu) (string)
        :param interval: Takes an interval by user (it cans be in some drop-down menu) (string)
        :return:
        """
        for ticker_symbol in self.__tickers_list:

            ticker = yf.Ticker(ticker_symbol)
            info = ticker.fast_info

            if ticker_symbol not in self.__collected_info:

                info_to_add = {
                    'currency': info.get('currency'),
                    'exchange': info.get('exchange'),
                    'lastPrice': info.get('lastPrice'),
                    'timezone': info.get('timezone')
                }

                self.__collected_info[ticker_symbol] = info_to_add

                historical_data = ticker.history(period=period, interval=interval)
                formatted_historical_data = self.__format_historical_data(historical_data, ticker_symbol)
                if formatted_historical_data:
                    self.__collected_info[ticker_symbol]['daily_info'] = formatted_historical_data

    def __format_historical_data(self, historical_data, ticker_symbol):
        """
        Formats historical data for a given ticker.
        :param historical_data: Historical data from yfinance.
        :param ticker_symbol: Symbol of ticker in string 'TSLA'
        :return:
        """
        formated_historical_data = {}

        if historical_data.empty or historical_data.dropna().empty:
            del self.__collected_info[ticker_symbol]
            return None

        for index, row in historical_data.iterrows():
            date_str = str(index.date())
            time_str = str(index.time())

            utc_time = convert_to_utc_time(time_str, date_str, self.__collected_info[ticker_symbol]['timezone'])

            close_value = row['Close']
            formated_historical_data[utc_time] = close_value
        return formated_historical_data

    def __process_fetching_info(self):
        """
        Process of fetching information for the tickers.

        Calls internal methods to obtain tickers and extract their information.
        :return:
        """
        self.__get_tickers_by_company()
        period, interval = prompt_user_to_paste_period_interval()
        self.__fetch_tickers_info(period=period, interval=interval)

    @property
    def collected_info(self):
        """
        Returns the collected information for the tickers
        :return: dict
        """
        self.__process_fetching_info()
        return self.__collected_info

    @property
    def tickers_list(self):
        """
        Returns a list of tickers associated with the searched company.
        :return: list
        """
        return self.__tickers_list
