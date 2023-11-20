from process_data import ProcessData
from helprers import record_in_json_file

prd = ProcessData()
class PrepareDataInRecordFormat:
    def __init__(self):
        self.__data_to_process = prd.collected_data
        # self.__data_to_process = {
        #     'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125,
        #              'timezone': 'America/New_York',
        #              'daily_info': {'2023-11-17 14:30:00': 144.55999755859375,
        #                             '2023-11-17 15:30:00': 144.20010375976562,
        #                             '2023-11-17 16:30:00': 144.3000030517578,
        #                             '2023-11-17 17:30:00': 144.7133026123047,
        #                             '2023-11-17 18:30:00': 144.74000549316406,
        #                             '2023-11-17 19:30:00': 144.56500244140625,
        #                             '2023-11-17 20:30:00': 145.17999267578125},
        #              'difference_in_USD_AMZN.MX': {'2023-11-17 14:30:00': '-0.14599428660136482 USD',
        #                                            '2023-11-17 15:30:00': '0.07033003860919962 USD',
        #                                            '2023-11-17 16:30:00': '0.14306321143442347 USD',
        #                                            '2023-11-17 17:30:00': '0.020393562885914207 USD',
        #                                            '2023-11-17 18:30:00': '0.20468118649878875 USD',
        #                                            '2023-11-17 19:30:00': '1.0400016423189413 USD'},
        #              'difference_in_USD_AMZN.NE': {'2023-11-17 14:30:00': '-131.79262120935275 USD',
        #                                            '2023-11-17 15:30:00': '-131.4473608409121 USD',
        #                                            '2023-11-17 16:30:00': '-131.54726013290428 USD',
        #                                            '2023-11-17 17:30:00': '-131.9239775130032 USD',
        #                                            '2023-11-17 18:30:00': '-131.94336367866882 USD',
        #                                            '2023-11-17 19:30:00': '-131.77567734210476 USD',
        #                                            '2023-11-17 20:30:00': '-132.34676728531733 USD'}},
        #     'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125,
        #                 'timezone': 'America/Mexico_City',
        #                 'daily_info': {'2023-11-17 14:30:00': 2484.5, '2023-11-17 15:30:00': 2482.030029296875,
        #                                '2023-11-17 16:30:00': 2485.0, '2023-11-17 17:30:00': 2490.0,
        #                                '2023-11-17 18:30:00': 2493.6298828125,
        #                                '2023-11-17 19:30:00': 2504.989990234375},
        #                 'difference_in_MXN_AMZN': {'2023-11-17 14:30:00': '21.743115567967834 MXN',
        #                                            '2023-11-17 15:30:00': '17.97359145315022 MXN',
        #                                            '2023-11-17 16:30:00': '16.73557922425016 MXN',
        #                                            '2023-11-17 17:30:00': '18.90097211150487 MXN',
        #                                            '2023-11-17 18:30:00': '15.73403833366092 MXN',
        #                                            '2023-11-17 19:30:00': '1.3398952098023074 MXN'},
        #                 'difference_in_MXN_AMZN.NE': {'2023-11-17 14:30:00': '-2265.564995794089 MXN',
        #                                               '2023-11-17 15:30:00': '-2263.34595919487 MXN',
        #                                               '2023-11-17 16:30:00': '-2266.315929897995 MXN',
        #                                               '2023-11-17 17:30:00': '-2270.688618568623 MXN',
        #                                               '2023-11-17 18:30:00': '-2274.19303432917 MXN',
        #                                               '2023-11-17 19:30:00': '-2285.678608802998 MXN'}},
        #     'AMZN.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 17.540000915527344,
        #                 'timezone': 'America/Toronto',
        #                 'daily_info': {'2023-11-17 14:30:00': 17.450000762939453,
        #                                '2023-11-17 15:30:00': 17.43000030517578,
        #                                '2023-11-17 16:30:00': 17.43000030517578,
        #                                '2023-11-17 17:30:00': 17.479999542236328,
        #                                '2023-11-17 18:30:00': 17.489999771118164,
        #                                '2023-11-17 19:30:00': 17.479999542236328,
        #                                '2023-11-17 20:30:00': 17.540000915527344},
        #                 'difference_in_CAD_AMZN': {'2023-11-17 14:30:00': '180.12951743133286 CAD',
        #                                            '2023-11-17 15:30:00': '179.65762770803352 CAD',
        #                                            '2023-11-17 16:30:00': '179.79416654528524 CAD',
        #                                            '2023-11-17 17:30:00': '180.3090506052769 CAD',
        #                                            '2023-11-17 18:30:00': '180.33554693438964 CAD',
        #                                            '2023-11-17 19:30:00': '180.10635914976297 CAD',
        #                                            '2023-11-17 20:30:00': '180.88690478985126 CAD'},
        #                 'difference_in_CAD_AMZN.MX': {'2023-11-17 14:30:00': '180.57464610781682 CAD',
        #                                               '2023-11-17 15:30:00': '180.39777996213215 CAD',
        #                                               '2023-11-17 16:30:00': '180.6344985774281 CAD',
        #                                               '2023-11-17 17:30:00': '180.98301945884361 CAD',
        #                                               '2023-11-17 18:30:00': '181.26233549566012 CAD',
        #                                               '2023-11-17 19:30:00': '182.17778199567525 CAD'}}}

        # self.__store_data_before_processed = sdbp.data_before_filter
        # self.__new_data = {}
        self.__final_data = []

    def __reformat_data_for_google_sheet(self):
        for ticker, ticker_data in self.__data_to_process.items():
            new_data = {'Company Ticker': ticker, 'Exchange Name': '', 'Local Company Timezone': '',
                        'Local Company Currency': '', 'Found time in Period in UTC': [],
                        'Close Prices in Local Currency': []}

            for key, value in ticker_data.items():
                if key == 'exchange':
                    new_data['Exchange Name'] = value
                elif key == 'timezone':
                    new_data['Local Company Timezone'] = value
                elif key == 'currency':
                    new_data['Local Company Currency'] = value
                elif key == 'daily_info':
                    for time, price in value.items():
                        new_data['Found time in Period in UTC'].append(time)
                        new_data['Close Prices in Local Currency'].append(price)

                elif key.startswith('difference_in_'):
                    take_other_ticker = key[len('difference_in_') + len(ticker_data['currency']) + 1:]
                    name_of_col = f"Difference in {ticker_data['currency']} with {take_other_ticker}"
                    if name_of_col not in new_data:
                        new_data[name_of_col] = []
                    for time, price in value.items():
                        new_data[name_of_col].append(price)

            self.__final_data.append(new_data)

    @property
    def final_data(self):
        self.__reformat_data_for_google_sheet()
        return self.__final_data


if __name__ == "__main__":
    # prd = PrepareDataInRecordFormat()
    # print(prd.final_data)
    test_data = [{'Company Ticker': 'AMZN', 'Exchange Name': 'NMS', 'Local Company Timezone': 'America/New_York',
                  'Local Company Currency': 'USD',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00', '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00', '2023-11-17 19:30:00',
                                                  '2023-11-17 20:30:00'],
                  'Close Prices in Local Currency': [144.55999755859375, 144.20010375976562, 144.3000030517578,
                                                     144.7133026123047, 144.74000549316406, 144.56500244140625,
                                                     145.17999267578125],
                  'Difference in USD with AMZN.MX': ['-0.14599428660136482 USD', '0.07033003860919962 USD',
                                                     '0.14306321143442347 USD', '0.020393562885914207 USD',
                                                     '0.20468118649878875 USD', '1.0400016423189413 USD'],
                  'Difference in USD with AMZN.NE': ['-131.79262120935275 USD', '-131.4473608409121 USD',
                                                     '-131.54726013290428 USD', '-131.9239775130032 USD',
                                                     '-131.94336367866882 USD', '-131.77567734210476 USD',
                                                     '-132.34676728531733 USD']},
                 {'Company Ticker': 'AMZN.MX', 'Exchange Name': 'MEX', 'Local Company Timezone': 'America/Mexico_City',
                  'Local Company Currency': 'MXN',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00', '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00', '2023-11-17 19:30:00'],
                  'Close Prices in Local Currency': [2484.5, 2482.030029296875, 2485.0, 2490.0, 2493.6298828125,
                                                     2504.989990234375],
                  'Difference in MXN with AMZN': ['21.743115567967834 MXN', '17.97359145315022 MXN',
                                                  '16.73557922425016 MXN', '18.90097211150487 MXN',
                                                  '15.73403833366092 MXN', '1.3398952098023074 MXN'],
                  'Difference in MXN with AMZN.NE': ['-2265.564995794089 MXN', '-2263.34595919487 MXN',
                                                     '-2266.315929897995 MXN', '-2270.688618568623 MXN',
                                                     '-2274.19303432917 MXN', '-2285.678608802998 MXN']},
                 {'Company Ticker': 'AMZN.NE', 'Exchange Name': 'NEO', 'Local Company Timezone': 'America/Toronto',
                  'Local Company Currency': 'CAD',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00', '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00', '2023-11-17 19:30:00',
                                                  '2023-11-17 20:30:00'],
                  'Close Prices in Local Currency': [17.450000762939453, 17.43000030517578, 17.43000030517578,
                                                     17.479999542236328, 17.489999771118164, 17.479999542236328,
                                                     17.540000915527344],
                  'Difference in CAD with AMZN': ['180.12951743133286 CAD', '179.65762770803352 CAD',
                                                  '179.79416654528524 CAD', '180.3090506052769 CAD',
                                                  '180.33554693438964 CAD', '180.10635914976297 CAD',
                                                  '180.88690478985126 CAD'],
                  'Difference in CAD with AMZN.MX': ['180.57464610781682 CAD', '180.39777996213215 CAD',
                                                     '180.6344985774281 CAD', '180.98301945884361 CAD',
                                                     '181.26233549566012 CAD', '182.17778199567525 CAD']}]

    record_in_json_file('some_test.json', test_data)


