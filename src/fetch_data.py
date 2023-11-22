
from src.ticker_data_processor import TickerDataProcessor
from src.ticker_fetcher import TickerFetcher
from src.ticker_library_manager import TickerLibraryManager
from src.helprers import prompt_user_to_paste_period_interval


class FetchData:
    """
    The FetchData class retrieves information about financial tickers.

    It fetches information for a given ticker or company name, including the last price,
    currency, exchange, and timezone. It also provides historical data for the ticker
    over a specified period and interval.
    Class uses 'yfinance' library.

    """

    def __init__(self, ticker_to_search: str):
        self.ticker_to_search = ticker_to_search.upper()
        self.__collected_info = {}
        self.__tickers_list = []
        self.__library_manager = TickerLibraryManager()
        self.__ticker_fetcher = TickerFetcher()
        self.__data_processor = TickerDataProcessor()

    def __fetch_data(self):
        """
        This method is responsible for fetching info from given ticker or company name
        :return:
        """
        if self.ticker_to_search.isspace():
            raise TypeError("Tocker/Company name can not be a whitespace or empty string!")

        try:
            self.__tickers_list = self.__library_manager.get_tickers_by_company(self.ticker_to_search)
        except ValueError as e:
            print(f"The ticker is not found! {e}")
            return

        period, interval = prompt_user_to_paste_period_interval()

        for ticker_symbol in self.__tickers_list:
            info, historical_data = self.__ticker_fetcher.fetch_ticker_info(ticker_symbol, period, interval)
            formatted_historical_data = self.__data_processor.format_historical_data(historical_data,
                                                                                     info.get('timezone', ''))

            self.__collected_info[ticker_symbol] = {
                'currency': info.get('currency'),
                'exchange': info.get('exchange'),
                'lastPrice': info.get('lastPrice'),
                'timezone': info.get('timezone'),
                'daily_info': formatted_historical_data
            }

    @property
    def collected_info(self):
        """
        Returns the collected information for the tickers
        :return: dict
        """
        self.__fetch_data()
        return self.__collected_info

    @property
    def tickers_list(self):
        """
        Returns a list of tickers associated with the searched company.
        :return: list
        """
        return self.__tickers_list
