from src.ticker_storage import TickerStorage

ts = TickerStorage()

class TickerLibraryManager:
    """
    Manages a library of stock tickers, providing functionality to retrieve ticker symbols based on a company's name.

    This class interfaces with a `TickerStorage` instance to access a collection of stock tickers. It is designed to
    offer an easy way to obtain all related ticker symbols for a given company.
    """
    def __init__(self):
        self.__library_with_tickers = ts.collection_stock_tickers

    def get_tickers_by_company(self, company_name):
        for company, tickers in self.__library_with_tickers.items():
            if company_name in tickers or company_name in company:
                return tickers
        raise ValueError(f"Company '{company_name}' not found in ticker library.")
