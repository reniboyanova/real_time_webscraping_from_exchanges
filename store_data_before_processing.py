from fetch_data import FetchData
from helprers import prompt_user_to_paste_ticker

fd = FetchData(prompt_user_to_paste_ticker())
class StoreDataBeforeProcessing:
    """
    StoreDataBeforeProcessing is designed to store and manage financial data before any filtering or processing.

    This class retrieves the raw financial data collected by FetchData and stores it in its original form.
    It provides a method to access this data before any filtering is applied.
    """
    def __init__(self):
        self.__data = fd.collected_info
        self.__data_before_filter = {}

    def __store_ticker_data_before_filter(self):
        for ticker, data in self.__data.items():
            self.__data_before_filter[ticker] = data['daily_info']

    @property
    def data_before_filter(self):
        """
        Public property to access the financial data before filtering.

        This property calls the private method __store_ticker_data_before_filter to ensure that
        the data is stored in its original form and then returns it.
        :return:
        """
        self.__store_ticker_data_before_filter()
        return self.__data_before_filter

