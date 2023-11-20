import json
from datetime import datetime

import pytz
import yfinance as yf
from forex_python.converter import CurrencyRates
from colections_of_tickers import CollectionsOfTickers as ct
from helprers import convert_to_utc_time, prompt_user_to_paste_period_interval

class FetchData:
    def __init__(self, ticker_to_search):
        self.ticker_to_search = ticker_to_search
        self.__library_with_tickers = ct().collection_stock_tickers
        self.__collected_info = {}
        self.__tickers_list = []

    def __get_tickers_by_company(self):
        for company, tickers in self.__library_with_tickers.items():
            if self.ticker_to_search in tickers or self.ticker_to_search in company:
                print("Find it!")
                self.__tickers_list = tickers
                print(self.__tickers_list)
                return
        raise ValueError(f"Ticker '{self.ticker_to_search}' not found in any company.")

    def __fetch_tickers_info(self, period, interval):
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
                formatted_historical_data = {}

                if historical_data.empty or historical_data.dropna().empty:
                    del self.__collected_info[ticker_symbol]
                    continue

                for index, row in historical_data.iterrows():
                    date_str = str(index.date())
                    time_str = str(index.time())

                    utc_time = convert_to_utc_time(time_str, date_str, self.__collected_info[ticker_symbol]['timezone'])

                    close_value = row['Close']
                    formatted_historical_data[utc_time] = close_value

                self.__collected_info[ticker_symbol]['daily_info'] = formatted_historical_data

    def __process_fetching_info(self):
        self.__get_tickers_by_company()
        period, interval = prompt_user_to_paste_period_interval()
        self.__fetch_tickers_info(period=period, interval=interval)

    @property
    def collected_info(self):
        self.__process_fetching_info()
        return self.__collected_info

    @property
    def tickers_list(self):
        return self.__tickers_list


if __name__ == "__main__":
    f_info = FetchData('AMZN')
    print(f_info.collected_info)
    print(f_info.tickers_list)

    test_data = {
        'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125, 'timezone': 'America/New_York',
                 'daily_info': {'2023-11-17 14:30:00': 144.55999755859375, '2023-11-17 15:30:00': 144.20010375976562,
                                '2023-11-17 16:30:00': 144.3000030517578, '2023-11-17 17:30:00': 144.7133026123047,
                                '2023-11-17 18:30:00': 144.74000549316406, '2023-11-17 19:30:00': 144.56500244140625,
                                '2023-11-17 20:30:00': 145.17999267578125}},
        'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125,
                    'timezone': 'America/Mexico_City',
                    'daily_info': {'2023-11-17 14:30:00': 2484.5, '2023-11-17 15:30:00': 2482.030029296875,
                                   '2023-11-17 16:30:00': 2485.0, '2023-11-17 17:30:00': 2490.0,
                                   '2023-11-17 18:30:00': 2493.6298828125, '2023-11-17 19:30:00': 2504.989990234375}},
        'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.8800048828125, 'timezone': 'Europe/Berlin',
                   'daily_info': {'2023-11-20 08:00:00': 132.8800048828125}},
        'AMZN.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 17.540000915527344,
                    'timezone': 'America/Toronto',
                    'daily_info': {'2023-11-17 14:30:00': 17.450000762939453, '2023-11-17 15:30:00': 17.43000030517578,
                                   '2023-11-17 16:30:00': 17.43000030517578, '2023-11-17 17:30:00': 17.479999542236328,
                                   '2023-11-17 18:30:00': 17.489999771118164, '2023-11-17 19:30:00': 17.479999542236328,
                                   '2023-11-17 20:30:00': 17.540000915527344}},
        'AMZO34.SA': {'currency': 'BRL', 'exchange': 'SAO', 'lastPrice': 35.4900016784668,
                      'timezone': 'America/Sao_Paulo', 'daily_info': {'2023-11-17 13:00:00': 34.970001220703125,
                                                                      '2023-11-17 14:00:00': 35.20000076293945,
                                                                      '2023-11-17 15:00:00': 35.31999969482422,
                                                                      '2023-11-17 16:00:00': 35.290000915527344,
                                                                      '2023-11-17 17:00:00': 35.33000183105469,
                                                                      '2023-11-17 18:00:00': 35.43000030517578,
                                                                      '2023-11-17 19:00:00': 35.400001525878906}},
        'AMZN.BA': {'currency': 'ARS', 'exchange': 'BUE', 'lastPrice': 885.5,
                    'timezone': 'America/Argentina/Buenos_Aires',
                    'daily_info': {'2023-11-17 14:00:00': 863.0, '2023-11-17 15:00:00': 859.0,
                                   '2023-11-17 16:00:00': 863.0, '2023-11-17 17:00:00': 858.0,
                                   '2023-11-17 18:00:00': 879.5, '2023-11-17 19:00:00': 885.5}}}
