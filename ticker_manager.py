from ticker_storage import TickerStorage


class TickerManager:
    """
    TickerManager manages the addition of new stock tickers to a storage system.

    It interacts with an instance of TickerStorage to add new ticker information.
    The class ensures that the data being added is in the correct format.
    """
    def __init__(self, storage: TickerStorage):
        self.storage = storage

    def add_tickers(self, new_ticker):
        """
        Adds a new ticker or set of tickers to the storage.
        Validates the input format, ensuring that the company name is a string and the tickers are a list.
        Raises a TypeError if the new ticker is not a dictionary and if the company name
        is not a string or the tickers are not a list.
        :param new_ticker: (dict): A dictionary with company names as keys and a list of tickers as values.
        :return:
        """
        if not isinstance(new_ticker, dict):
            raise TypeError("New ticker must be a dictionary.")

        for company, tickers in new_ticker.items():
            if not isinstance(company, str) or not isinstance(tickers, list):
                raise TypeError("Company must be a string and tickers must be a list.")
            self.storage.add_tickers(company, tickers)

