import json


class TickerStorage:
    """
    TickerStorage stores and manages a collection of stock tickers.
    This class maintains a private dictionary of stock tickers, indexed by company names.
    It provides methods to retrieve and update this ticker collection
    """

    def __init__(self):
        with open("companies_info.json", "r") as file:
            self.__collection_stock_tickers = json.load(file)

    @property
    def collection_stock_tickers(self):
        """
        Provides access to the collection of stock tickers.
        :return:
        """
        return self.__collection_stock_tickers

    def add_tickers(self, company, tickers):
        """
        Adds new tickers for a company to the collection.

        If the company does not exist in the collection, it adds the new company and tickers.
        If the company already exists, it extends the existing list with new tickers,
        avoiding duplicates.
        :param company: Company name (string)
        :param tickers: List with new tickers (list)
        :return:
        """

        if company not in self.__collection_stock_tickers:
            self.__collection_stock_tickers[company] = tickers
        else:
            self.__collection_stock_tickers[company].extend(
                [t for t in tickers if t not in self.__collection_stock_tickers[company]])
