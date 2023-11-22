from process_data import ProcessData

prd = ProcessData()


class PrepareDataInRecordFormat:
    """
    This class is responsible for reformatting financial data into a structure suitable for exporting to Google Sheets.

    It processes data collected from financial tickers and transforms it into a format that is easier to work with for
    visualization and analysis purposes.

    """

    def __init__(self):
        self.__data_to_process = prd.collected_data
        self.__final_data = []

    @staticmethod
    def __format_exchange(ticker_data):
        """
        Extracts and returns the exchange name from the ticker data.
        :param ticker_data: (dict) A dictionary containing data for a single ticker.
        :return:
        """
        return ticker_data.get('exchange', '')

    @staticmethod
    def __format_timezone(ticker_data):
        """
        Extracts and returns the currency from the ticker data.
        :param ticker_data: (dict) A dictionary containing data for a single ticker.
        :return:
        """
        return ticker_data.get('timezone', '')

    @staticmethod
    def __format_currency(ticker_data):
        """
        Extracts daily information from the ticker data.
        :param ticker_data: (dict): A dictionary containing data for a single ticker.
        :return:
        """
        return ticker_data.get('currency', '')

    @staticmethod
    def __format_daily_info(ticker_data):
        return ticker_data.get('daily_info', '')

    @staticmethod
    def __format_differences(ticker_data):
        """
        Extracts and formats price differences from the ticker data.
        :param ticker_data: (dict): A dictionary containing data for a single ticker.
        :return:
        """
        differences = {}
        for key, value in ticker_data.items():
            if key.startswith('difference_in_'):
                take_other_ticker = key[len('difference_in_') + len(ticker_data['currency']) + 1:]
                name_of_col = f"Difference in {ticker_data['currency']} with {take_other_ticker}"
                differences[name_of_col] = [price for time, price in value.items()]
        return differences

    def __reformat_data_for_google_sheet(self):
        """
        Reformats the raw data into a structure suitable for Google Sheets.
        This method processes each ticker's data and transforms it into a more
        structured format, adding it to the __final_data list.
        :return:
        """
        for ticker, ticker_data in self.__data_to_process.items():
            new_data = {'Company Ticker': ticker,
                        'Exchange Name': self.__format_exchange(ticker_data),
                        'Local Company Timezone': self.__format_timezone(ticker_data),
                        'Local Company Currency': self.__format_currency(ticker_data),
                        'Found Periods (UTC)': [],
                        'Close Prices in Local Currency': []}

            for time, price in self.__format_daily_info(ticker_data).items():
                new_data['Found Periods (UTC)'].append(time)
                new_data['Close Prices in Local Currency'].append(price)

            differences_in_price = self.__format_differences(ticker_data)
            new_data.update(differences_in_price)

            self.__final_data.append(new_data)

    @property
    def final_data(self):
        """
        Returns the reformatted data ready for export.
        This property ensures that data reformatting is executed before accessing the final data.
        :return:
        """
        self.__reformat_data_for_google_sheet()
        return self.__final_data
