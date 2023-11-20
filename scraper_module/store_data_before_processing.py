from fetch_data import FetchData as fd
class StoreDataBeforeProcessing:
    def __init__(self):
        # self.__data = fd.collected_info
        self.__data = {
            'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125,
                     'timezone': 'America/New_York',
                     'daily_info': {'2023-11-17 14:30:00': 144.55999755859375,
                                    '2023-11-17 15:30:00': 144.20010375976562,
                                    '2023-11-17 16:30:00': 144.3000030517578, '2023-11-17 17:30:00': 144.7133026123047,
                                    '2023-11-17 18:30:00': 144.74000549316406,
                                    '2023-11-17 19:30:00': 144.56500244140625,
                                    '2023-11-17 20:30:00': 145.17999267578125}},
            'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125,
                        'timezone': 'America/Mexico_City',
                        'daily_info': {'2023-11-17 14:30:00': 2484.5, '2023-11-17 15:30:00': 2482.030029296875,
                                       '2023-11-17 16:30:00': 2485.0, '2023-11-17 17:30:00': 2490.0,
                                       '2023-11-17 18:30:00': 2493.6298828125,
                                       '2023-11-17 19:30:00': 2504.989990234375}},
            'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.8800048828125,
                       'timezone': 'Europe/Berlin',
                       'daily_info': {'2023-11-20 08:00:00': 132.8800048828125}},
            'AMZN.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 17.540000915527344,
                        'timezone': 'America/Toronto',
                        'daily_info': {'2023-11-17 14:30:00': 17.450000762939453,
                                       '2023-11-17 15:30:00': 17.43000030517578,
                                       '2023-11-17 16:30:00': 17.43000030517578,
                                       '2023-11-17 17:30:00': 17.479999542236328,
                                       '2023-11-17 18:30:00': 17.489999771118164,
                                       '2023-11-17 19:30:00': 17.479999542236328,
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
        self.__data_before_filter = {}


    def __store_ticker_data_before_filter(self):
        for ticker, data in self.__data.items():
            self.__data_before_filter[ticker] = data['daily_info']


    @property
    def data_before_filter(self):
        self.__store_ticker_data_before_filter()
        return self.__data_before_filter


if __name__ == "__main__":
    st_data = StoreDataBeforeProcessing()
    print(st_data.data_before_filter)