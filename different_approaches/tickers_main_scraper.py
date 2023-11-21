from scraper_module.helprers import get_api_key
from defines_ import Defines as de

from alpha_vantage.timeseries import TimeSeries
import requests
from requests import RequestException

class TickersMainScraper:
    """
    Class TickersMainScraper use Alpha Vantage API to handle different stocks info
     from exchange markets all around the world.
     This API is a free version, so keep in mind that it has only 25 requests by day.
    """

    def __init__(self):
        self.__api_kay = get_api_key(de.api_key_file)
        self.__ts = TimeSeries(key=self.__api_kay, output_format='pandas')
        self.ticker_container = []
        self.company_info_from_different_exchanges = {}

        self.arbitrage = {}

    # first step
    def __fill_ticker_container(self, needed_20_positions):
        conf_url = f'{de.gs_ls_most_act_url}{self.__api_kay}'
        try:
            response = requests.get(conf_url)
            data = response.json()
            key = de.gs_ls_most_act[
                needed_20_positions] if needed_20_positions in de.gs_ls_most_act else 'most_actively_traded'
            self.ticker_container = [ticker['ticker'] for ticker in data[key]]
        except RequestException as e:
            print(f"Exception was occurred: {e}")

    # second step:
    def __find_best_matches(self, company_or_ticker_search=None):
        url = f'{de.best_matches_url}{self.__api_kay}'

        if company_or_ticker_search:
            tickers_to_search = [company_or_ticker_search]
        else:
            tickers_to_search = self.ticker_container

        for ticker in tickers_to_search:
            params = {
                "function": "SYMBOL_SEARCH",
                "keywords": ticker,
                "apikey": self.__api_kay,
                "datatype": "json"
            }
            try:
                response = requests.get(url, params=params)
                data = response.json()

                # self.company_info_from_different_exchanges[ticker] = []

                for match in data['bestMatches']:
                    info = {
                        'symbol': match.get('1. symbol', ''),
                        'name': match.get('2. name', ''),
                        'timezone': match.get('7. timezone', ''),
                        'currency': match.get('8. currency', '')
                    }
                    # print(info)
                    self.company_info_from_different_exchanges[match] = {info}

            except RequestException as e:
                print(f"Error war occurred: {e}")
        print(self.company_info_from_different_exchanges)




    # third step (search daily info for all companies)
    def __last_close_info(self):
        for info in self.company_info_from_different_exchanges.values():
            for el in info:
                print(el)
                symbol = el.get('symbol')
                print(symbol)
                # IBM&interval=5min&apikey=demo
                #https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
                url = f'{de.time_daily_info_url}{symbol}&apikey={self.__api_kay}'
                print(url)
                try:
                    response = requests.get(url)
                    data = response.json()
                    time_series = data.get("Time Series (5min)", {})

                    close_data = {}
                    for date, values in time_series.items():
                        print(date)
                        if date not in close_data:
                            close_data[date] = {}
                        close_data[date] = values.get("4. close")

                    el["daily_info"] = close_data  # Corrected line

                except RequestException as e:
                    print(f"Error occurred while fetching last close info: {e}")

    def __collect_sequentially_info(self):
        # type_of_market_position = input("Choose between - Top gainers, losers, and most actively traded US tickers:"
        #                                 "\nInsert:\ngainers, losers or most-actives\n")
        # self.__fill_ticker_container(type_of_market_position)
        print(self.ticker_container)

        symbol = input("Choose your symbol: ")
        self.__find_best_matches(symbol)

        # print(self.company_info_from_different_exchanges)
        # self.__last_close_info()

    def print_data(self):
        self.__collect_sequentially_info()
        print(self.company_info_from_different_exchanges)


if __name__ == "__main__":
    # test_dict = {'tesla': [{'symbol': 'TSLA', 'name': 'Tesla Inc', 'timezone': 'UTC-04', 'currency': 'USD',
    # 'daily_info': {'2023-11-17': {'19:55:00': '233.9900', '19:50:00': '233.9600', '19:45:00': '234.0550', '19:40:00': '234.0900', '19:35:00': '234.1000', '19:30:00': '233.9500', '19:25:00': '233.9100', '19:20:00': '234.1900', '19:15:00': '234.1500', '19:10:00': '234.0800', '19:05:00': '233.9800', '19:00:00': '233.8000', '18:55:00': '233.7900', '18:50:00': '233.7300', '18:45:00': '233.8350', '18:40:00': '233.8850', '18:35:00': '233.8350', '18:30:00': '233.9000', '18:25:00': '233.8800', '18:20:00': '233.9200', '18:15:00': '233.8050', '18:10:00': '233.8300', '18:05:00': '233.8800', '18:00:00': '233.8500', '17:55:00': '233.6700', '17:50:00': '233.7800', '17:45:00': '234.0300', '17:40:00': '234.0300', '17:35:00': '234.1000', '17:30:00': '234.1300', '17:25:00': '234.1000', '17:20:00': '234.2460', '17:15:00': '234.0500', '17:10:00': '234.1200', '17:05:00': '233.9350', '17:00:00': '233.7900', '16:55:00': '233.8400', '16:50:00': '233.6800', '16:45:00': '233.6300', '16:40:00': '233.7000', '16:35:00': '233.8700', '16:30:00': '233.6200', '16:25:00': '233.5800', '16:20:00': '233.7000', '16:15:00': '234.3000', '16:10:00': '233.7000', '16:05:00': '233.7500', '16:00:00': '234.0600', '15:55:00': '234.4800', '15:50:00': '234.7200', '15:45:00': '234.1900', '15:40:00': '234.5800', '15:35:00': '234.2820', '15:30:00': '234.5830', '15:25:00': '234.6880', '15:20:00': '235.3300', '15:15:00': '234.3800', '15:10:00': '234.4860', '15:05:00': '234.8600', '15:00:00': '234.9470', '14:55:00': '234.6570', '14:50:00': '233.9260', '14:45:00': '233.8900', '14:40:00': '234.1100', '14:35:00': '233.9350', '14:30:00': '234.9800', '14:25:00': '235.1100', '14:20:00': '234.8100', '14:15:00': '234.3600', '14:10:00': '234.8750', '14:05:00': '235.5890', '14:00:00': '236.1000', '13:55:00': '235.9000', '13:50:00': '235.3100', '13:45:00': '236.1100', '13:40:00': '236.2600', '13:35:00': '237.0470', '13:30:00': '237.3500', '13:25:00': '236.5200', '13:20:00': '236.3400', '13:15:00': '236.8610', '13:10:00': '236.7100', '13:05:00': '236.5800', '13:00:00': '235.9200', '12:55:00': '236.2700', '12:50:00': '235.5930', '12:45:00': '235.2090', '12:40:00': '235.2750', '12:35:00': '234.8510', '12:30:00': '234.4250', '12:25:00': '234.7000', '12:20:00': '234.8400', '12:15:00': '235.2900', '12:10:00': '235.0500', '12:05:00': '234.9340', '12:00:00': '235.0500', '11:55:00': '235.2310', '11:50:00': '234.4690', '11:45:00': '234.5500', '11:40:00': '234.7760'}}}, {'symbol': 'TL0.DEX', 'name': 'Tesla Inc', 'timezone': 'UTC+02', 'currency': 'EUR', 'daily_info': {}}, {'symbol': 'TL0.FRK', 'name': 'Tesla Inc', 'timezone': 'UTC+02', 'currency': 'EUR', 'daily_info': {}}, {'symbol': 'TSLA34.SAO', 'name': 'Tesla Inc', 'timezone': 'UTC-03', 'currency': 'BRL', 'daily_info': {}}, {'symbol': 'TL01.FRK', 'name': 'TESLA INC. CDR DL-001', 'timezone': 'UTC+02', 'currency': 'EUR', 'daily_info': {}}]}

    # prime_time_zone = 'UTC-04'
    # for list_with_info in test_dict.values():
    #     for company in list_with_info:
    #         print(company)
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLAinterval=5min&apikey=T2RPXU9Z7B11EIAT'
    r = requests.get(url)
    data = r.json()
    print(data)
    # tickers_scr = TickersMainScraper()
    # tickers_scr.print_data()
