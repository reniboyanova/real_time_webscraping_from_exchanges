from src.fetch_data import FetchData
from src.data_cleaner import DataCleaner
from src.filer_data import DataFilter
from src.arbitrage_calculator import ArbitrageCalculator
from src.helprers import prompt_user_to_paste_ticker

fd = FetchData(prompt_user_to_paste_ticker())

class ProcessData:
    """
    This class is responsible for processing financial data related to stock tickers.

    It involves filtering the data, calculating potential arbitrage opportunities,
    and cleaning the data for final presentation or further analysis.

    The processing steps are carried out through interactions with other classes
    such as DataFilter, ArbitrageCalculator, and DataCleaner.
    """
    def __init__(self):
        self.__collected_data = fd.collected_info
        self.__list_with_tickers = fd.tickers_list

    def __process_data(self):
        """
        Initializes the ProcessData class by fetching data using the FetchData class.
        :return:
        """
        data_filter = DataFilter(self.__collected_data)
        data_filter.filter_based_on_longest_daily_info()

        arbitrage_calculator = ArbitrageCalculator(self.__collected_data, self.__list_with_tickers)
        arbitrage_calculator.add_arbitrage_opportunities()

        self.__collected_data = DataCleaner.clean_data(self.__collected_data)

    @property
    def collected_data(self):
        """
        Returns the processed data after applying filtering, arbitrage calculation, and cleaning.
        This property ensures the data processing steps are executed before accessing the final processed data.
        :return: dict: The processed data ready for analysis or export.
        """
        self.__process_data()
        return self.__collected_data
