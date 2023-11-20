from itertools import combinations

from fetch_data import FetchData
from helprers import convert_currency, prompt_user_to_paste_ticker

fd = FetchData(prompt_user_to_paste_ticker())


class ProcessData:
    def __init__(self):
        self.__collected_data = fd.collected_info
        self.__list_with_tickers = fd.tickers_list
        # self.__collected_data = {
        #     'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125,
        #              'timezone': 'America/New_York',
        #              'daily_info': {'2023-11-17 14:30:00': 144.55999755859375,
        #                             '2023-11-17 15:30:00': 144.20010375976562,
        #                             '2023-11-17 16:30:00': 144.3000030517578, '2023-11-17 17:30:00': 144.7133026123047,
        #                             '2023-11-17 18:30:00': 144.74000549316406,
        #                             '2023-11-17 19:30:00': 144.56500244140625,
        #                             '2023-11-17 20:30:00': 145.17999267578125}},
        #     'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125,
        #                 'timezone': 'America/Mexico_City',
        #                 'daily_info': {'2023-11-17 14:30:00': 2484.5, '2023-11-17 15:30:00': 2482.030029296875,
        #                                '2023-11-17 16:30:00': 2485.0, '2023-11-17 17:30:00': 2490.0,
        #                                '2023-11-17 18:30:00': 2493.6298828125,
        #                                '2023-11-17 19:30:00': 2504.989990234375}},
        #     'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.8800048828125,
        #                'timezone': 'Europe/Berlin',
        #                'daily_info': {'2023-11-20 08:00:00': 132.8800048828125}},
        #     'AMZN.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 17.540000915527344,
        #                 'timezone': 'America/Toronto',
        #                 'daily_info': {'2023-11-17 14:30:00': 17.450000762939453,
        #                                '2023-11-17 15:30:00': 17.43000030517578,
        #                                '2023-11-17 16:30:00': 17.43000030517578,
        #                                '2023-11-17 17:30:00': 17.479999542236328,
        #                                '2023-11-17 18:30:00': 17.489999771118164,
        #                                '2023-11-17 19:30:00': 17.479999542236328,
        #                                '2023-11-17 20:30:00': 17.540000915527344}},
        #     'AMZO34.SA': {'currency': 'BRL', 'exchange': 'SAO', 'lastPrice': 35.4900016784668,
        #                   'timezone': 'America/Sao_Paulo', 'daily_info': {'2023-11-17 13:00:00': 34.970001220703125,
        #                                                                   '2023-11-17 14:00:00': 35.20000076293945,
        #                                                                   '2023-11-17 15:00:00': 35.31999969482422,
        #                                                                   '2023-11-17 16:00:00': 35.290000915527344,
        #                                                                   '2023-11-17 17:00:00': 35.33000183105469,
        #                                                                   '2023-11-17 18:00:00': 35.43000030517578,
        #                                                                   '2023-11-17 19:00:00': 35.400001525878906}},
        #     'AMZN.BA': {'currency': 'ARS', 'exchange': 'BUE', 'lastPrice': 885.5,
        #                 'timezone': 'America/Argentina/Buenos_Aires',
        #                 'daily_info': {'2023-11-17 14:00:00': 863.0, '2023-11-17 15:00:00': 859.0,
        #                                '2023-11-17 16:00:00': 863.0, '2023-11-17 17:00:00': 858.0,
        #                                '2023-11-17 18:00:00': 879.5, '2023-11-17 19:00:00': 885.5}}}
        # self.__list_with_tickers = ['AMZN', 'AMZN.MX', 'AMZ.DE', 'AMZN.NE', 'AMZO34.SA', 'AMZN.BA']
        # self.__currencies = set()

    # def __filter_by_repeating_periods(self):
    #     repeated_periods = [set(info['daily_info'].keys()) for info in self.__collected_data.values()]
    #
    #     repeated_periods_in_all_data = set.intersection(*repeated_periods)
    #     # print(repeated_periods_in_all_data)
    #     for ticker, info in self.__collected_data.items():
    #         filtered_daily_info = {time: value for time, value in info['daily_info'].items() if
    #                                time in repeated_periods_in_all_data}
    #         self.__collected_data[ticker]['daily_info'] = filtered_daily_info

    # def __take_currencies(self):
    #     for ticker, ticker_info in self.__collected_data.items():
    #         self.__currencies.add(ticker_info['currency'])

    def __get_longest_daily_info(self):
        return max(self.__collected_data, key=lambda ticker: len(self.__collected_data[ticker]['daily_info']))

    def __create_subsets_based_on_longest(self, longest_daily_info_ticker):
        longest_daily_info = self.__collected_data[longest_daily_info_ticker]['daily_info']
        for ticker, info in self.__collected_data.items():
            if ticker != longest_daily_info_ticker:
                filtered_daily_info = {time: value for time, value in info['daily_info'].items() if
                                       time in longest_daily_info}
                self.__collected_data[ticker]['daily_info'] = filtered_daily_info

    def __add_arbitrage_opportunities(self):
        longest_daily_info_ticker = self.__get_longest_daily_info()
        self.__create_subsets_based_on_longest(longest_daily_info_ticker)
        ticker_pairs = list(combinations(self.__list_with_tickers, 2))

        for pair in ticker_pairs:
            ticker1, ticker2 = pair
            for time in self.__collected_data[ticker1]['daily_info']:
                if time in self.__collected_data[ticker2]['daily_info']:
                    price1 = self.__collected_data[ticker1]['daily_info'][time]
                    price2 = self.__collected_data[ticker2]['daily_info'][time]
                    currency_1 = self.__collected_data[ticker1]['currency']
                    currency_2 = self.__collected_data[ticker2]['currency']
                    date = time.split(' ')[0]

                    converted_price1 = convert_currency(from_currency=currency_2, to_currency=currency_1, amount=price2,
                                                        date_str=date)
                    converted_price2 = convert_currency(from_currency=currency_1, to_currency=currency_2, amount=price1,
                                                        date_str=date)

                    # Just to be easier, I made it str to add currency
                    price_diff_1 = str(converted_price1 - price1) + f' {currency_1}'
                    price_diff_2 = str(converted_price2 - price2) + f' {currency_2}'

                    self.__collected_data[ticker1].setdefault(f'difference_in_{currency_1}_{ticker2}', {})[
                        time] = price_diff_1

                    self.__collected_data[ticker2].setdefault(f'difference_in_{currency_2}_{ticker1}', {})[
                        time] = price_diff_2

    def __clean_data(self):
        self.__collected_data = {ticker: data for ticker, data in self.__collected_data.items() if data['daily_info']}

    def __process_data(self):
        self.__add_arbitrage_opportunities()
        self.__clean_data()

    @property
    def collected_data(self):
        self.__process_data()
        return self.__collected_data


if __name__ == "__main__":
    p_data = ProcessData()
    print(p_data.collected_data)

    processed_data = {
        'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125, 'timezone': 'America/New_York',
                 'daily_info': {'2023-11-17 14:30:00': 144.55999755859375, '2023-11-17 15:30:00': 144.20010375976562,
                                '2023-11-17 16:30:00': 144.3000030517578, '2023-11-17 17:30:00': 144.7133026123047,
                                '2023-11-17 18:30:00': 144.74000549316406, '2023-11-17 19:30:00': 144.56500244140625,
                                '2023-11-17 20:30:00': 145.17999267578125},
                 'difference_in_USD_AMZN.MX': {'2023-11-17 14:30:00': '-0.14599428660136482 USD',
                                               '2023-11-17 15:30:00': '0.07033003860919962 USD',
                                               '2023-11-17 16:30:00': '0.14306321143442347 USD',
                                               '2023-11-17 17:30:00': '0.020393562885914207 USD',
                                               '2023-11-17 18:30:00': '0.20468118649878875 USD',
                                               '2023-11-17 19:30:00': '1.0400016423189413 USD'},
                 'difference_in_USD_AMZN.NE': {'2023-11-17 14:30:00': '-131.79262120935275 USD',
                                               '2023-11-17 15:30:00': '-131.4473608409121 USD',
                                               '2023-11-17 16:30:00': '-131.54726013290428 USD',
                                               '2023-11-17 17:30:00': '-131.9239775130032 USD',
                                               '2023-11-17 18:30:00': '-131.94336367866882 USD',
                                               '2023-11-17 19:30:00': '-131.77567734210476 USD',
                                               '2023-11-17 20:30:00': '-132.34676728531733 USD'}},
        'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125,
                    'timezone': 'America/Mexico_City',
                    'daily_info': {'2023-11-17 14:30:00': 2484.5, '2023-11-17 15:30:00': 2482.030029296875,
                                   '2023-11-17 16:30:00': 2485.0, '2023-11-17 17:30:00': 2490.0,
                                   '2023-11-17 18:30:00': 2493.6298828125, '2023-11-17 19:30:00': 2504.989990234375},
                    'difference_in_MXN_AMZN': {'2023-11-17 14:30:00': '21.743115567967834 MXN',
                                               '2023-11-17 15:30:00': '17.97359145315022 MXN',
                                               '2023-11-17 16:30:00': '16.73557922425016 MXN',
                                               '2023-11-17 17:30:00': '18.90097211150487 MXN',
                                               '2023-11-17 18:30:00': '15.73403833366092 MXN',
                                               '2023-11-17 19:30:00': '1.3398952098023074 MXN'},
                    'difference_in_MXN_AMZN.NE': {'2023-11-17 14:30:00': '-2265.564995794089 MXN',
                                                  '2023-11-17 15:30:00': '-2263.34595919487 MXN',
                                                  '2023-11-17 16:30:00': '-2266.315929897995 MXN',
                                                  '2023-11-17 17:30:00': '-2270.688618568623 MXN',
                                                  '2023-11-17 18:30:00': '-2274.19303432917 MXN',
                                                  '2023-11-17 19:30:00': '-2285.678608802998 MXN'}},
        'AMZN.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 17.540000915527344,
                    'timezone': 'America/Toronto',
                    'daily_info': {'2023-11-17 14:30:00': 17.450000762939453, '2023-11-17 15:30:00': 17.43000030517578,
                                   '2023-11-17 16:30:00': 17.43000030517578, '2023-11-17 17:30:00': 17.479999542236328,
                                   '2023-11-17 18:30:00': 17.489999771118164, '2023-11-17 19:30:00': 17.479999542236328,
                                   '2023-11-17 20:30:00': 17.540000915527344},
                    'difference_in_CAD_AMZN': {'2023-11-17 14:30:00': '180.12951743133286 CAD',
                                               '2023-11-17 15:30:00': '179.65762770803352 CAD',
                                               '2023-11-17 16:30:00': '179.79416654528524 CAD',
                                               '2023-11-17 17:30:00': '180.3090506052769 CAD',
                                               '2023-11-17 18:30:00': '180.33554693438964 CAD',
                                               '2023-11-17 19:30:00': '180.10635914976297 CAD',
                                               '2023-11-17 20:30:00': '180.88690478985126 CAD'},
                    'difference_in_CAD_AMZN.MX': {'2023-11-17 14:30:00': '180.57464610781682 CAD',
                                                  '2023-11-17 15:30:00': '180.39777996213215 CAD',
                                                  '2023-11-17 16:30:00': '180.6344985774281 CAD',
                                                  '2023-11-17 17:30:00': '180.98301945884361 CAD',
                                                  '2023-11-17 18:30:00': '181.26233549566012 CAD',
                                                  '2023-11-17 19:30:00': '182.17778199567525 CAD'}}}
