import pandas as pd
import datetime
# import requests
# from requests.exceptions import ConnectionError
# from bs4 import BeautifulSoup
import yfinance as yf


class RealTimeScraper:
    def __init__(self):
        self.compare_prices = {}

    def get_real_time_stock_price(self, stock_index: str):
        current_ticker = yf.Ticker(stock_index)

        print(type(current_ticker.info))


if __name__ == "__main__":
    # import yfinance as yf

    ticker_tsla = yf.Ticker("TSLA")
    ticker_googl = yf.Ticker("GOOGL")
    print(ticker_googl.info)

    # data_nyse = ticker_tsla.history(period="1d")
    # data_nasdaq = ticker_googl.history(period="1d")
    #
    # print("TSLA Price on NYSE:")
    # print(data_nyse['Close'])
    #
    # print("GOOGLE Price on NASDAQ:")
    # print(data_nasdaq['Close'])
