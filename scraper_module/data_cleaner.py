class DataCleaner:
    """
    Static class. Clean providing data
    """
    @staticmethod
    def clean_data(collected_data):
        """
        Function that cleans proving data (dict) and leaves in it only tickers with existing daily info.
        Uses dictionary comprehension.
        :param collected_data: dictionary with collected data
        :return: same dictionary only with daily info tickers.
        """
        if not isinstance(collected_data, dict):
            raise TypeError("Data needs to be a dictionary!")
        return {ticker: data for ticker, data in collected_data.items() if data['daily_info']}
