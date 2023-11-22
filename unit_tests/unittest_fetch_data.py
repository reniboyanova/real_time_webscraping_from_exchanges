import json
import unittest
from fetch_data import FetchData
from ticker_data_processor import TickerDataProcessor
from ticker_fetcher import TickerFetcher
from ticker_library_manager import TickerLibraryManager


class TestFetchData(unittest.TestCase):
    __library_manager = {}
    test_data = {
        'GOOG': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 138.6199951171875, 'timezone': 'America/New_York',
                 'daily_info': {'2023-10-23 04:00:00': 137.89999389648438, '2023-10-24 04:00:00': 140.1199951171875,
                                '2023-10-25 04:00:00': 126.66999816894531, '2023-10-26 04:00:00': 123.44000244140625,
                                '2023-10-27 04:00:00': 123.4000015258789, '2023-10-30 04:00:00': 125.75,
                                '2023-10-31 04:00:00': 125.30000305175781, '2023-11-01 04:00:00': 127.56999969482422,
                                '2023-11-02 04:00:00': 128.5800018310547, '2023-11-03 04:00:00': 130.3699951171875,
                                '2023-11-06 05:00:00': 131.4499969482422, '2023-11-07 05:00:00': 132.39999389648438,
                                '2023-11-08 05:00:00': 133.25999450683594, '2023-11-09 05:00:00': 131.69000244140625,
                                '2023-11-10 05:00:00': 134.05999755859375, '2023-11-13 05:00:00': 133.63999938964844,
                                '2023-11-14 05:00:00': 135.42999267578125, '2023-11-15 05:00:00': 136.3800048828125,
                                '2023-11-16 05:00:00': 138.6999969482422, '2023-11-17 05:00:00': 136.94000244140625,
                                '2023-11-20 05:00:00': 137.9199981689453, '2023-11-21 05:00:00': 138.6199951171875}},
        'GOOGL': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 136.97000122070312, 'timezone': 'America/New_York',
                  'daily_info': {'2023-10-23 04:00:00': 136.5, '2023-10-24 04:00:00': 138.80999755859375,
                                 '2023-10-25 04:00:00': 125.61000061035156, '2023-10-26 04:00:00': 122.27999877929688,
                                 '2023-10-27 04:00:00': 122.16999816894531, '2023-10-30 04:00:00': 124.45999908447266,
                                 '2023-10-31 04:00:00': 124.08000183105469, '2023-11-01 04:00:00': 126.44999694824219,
                                 '2023-11-02 04:00:00': 127.48999786376953, '2023-11-03 04:00:00': 129.10000610351562,
                                 '2023-11-06 05:00:00': 130.25, '2023-11-07 05:00:00': 130.97000122070312,
                                 '2023-11-08 05:00:00': 131.83999633789062, '2023-11-09 05:00:00': 130.24000549316406,
                                 '2023-11-10 05:00:00': 132.58999633789062, '2023-11-13 05:00:00': 132.08999633789062,
                                 '2023-11-14 05:00:00': 133.6199951171875, '2023-11-15 05:00:00': 134.6199951171875,
                                 '2023-11-16 05:00:00': 136.92999267578125, '2023-11-17 05:00:00': 135.30999755859375,
                                 '2023-11-20 05:00:00': 136.25, '2023-11-21 05:00:00': 136.97000122070312}},
        'ABEA.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 125.76000213623047, 'timezone': 'Europe/Berlin',
                    'daily_info': {'2023-10-22 22:00:00': 128.22000122070312, '2023-10-23 22:00:00': 131.22000122070312,
                                   '2023-10-24 22:00:00': 119.4000015258789, '2023-10-25 22:00:00': 116.80000305175781,
                                   '2023-10-26 22:00:00': 115.18000030517578, '2023-10-29 23:00:00': 117.33999633789062,
                                   '2023-10-30 23:00:00': 116.55999755859375, '2023-10-31 23:00:00': 118.5999984741211,
                                   '2023-11-01 23:00:00': 119.94000244140625, '2023-11-02 23:00:00': 120.44000244140625,
                                   '2023-11-05 23:00:00': 120.66000366210938, '2023-11-06 23:00:00': 122.73999786376953,
                                   '2023-11-07 23:00:00': 122.9800033569336, '2023-11-08 23:00:00': 123.23999786376953,
                                   '2023-11-09 23:00:00': 122.87999725341797, '2023-11-12 23:00:00': 123.5,
                                   '2023-11-13 23:00:00': 123.9800033569336, '2023-11-14 23:00:00': 123.9000015258789,
                                   '2023-11-15 23:00:00': 125.33999633789062, '2023-11-16 23:00:00': 123.4000015258789,
                                   '2023-11-19 23:00:00': 124.4000015258789, '2023-11-20 23:00:00': 124.5199966430664,
                                   '2023-11-21 23:00:00': 125.76000213623047}},
        'GOOG.NE': {'currency': 'CAD', 'exchange': 'NEO', 'lastPrice': 23.420000076293945,
                    'timezone': 'America/Toronto',
                    'daily_info': {'2023-10-23 04:00:00': 23.329999923706055, '2023-10-24 04:00:00': 23.700000762939453,
                                   '2023-10-25 04:00:00': 21.40999984741211, '2023-10-26 04:00:00': 20.860000610351562,
                                   '2023-10-27 04:00:00': 20.84000015258789, '2023-10-30 04:00:00': 21.260000228881836,
                                   '2023-10-31 04:00:00': 21.15999984741211, '2023-11-01 04:00:00': 21.559999465942383,
                                   '2023-11-02 04:00:00': 21.719999313354492, '2023-11-03 04:00:00': 22.040000915527344,
                                   '2023-11-06 05:00:00': 22.209999084472656, '2023-11-07 05:00:00': 22.3799991607666,
                                   '2023-11-08 05:00:00': 22.489999771118164, '2023-11-09 05:00:00': 22.219999313354492,
                                   '2023-11-10 05:00:00': 22.610000610351562, '2023-11-13 05:00:00': 22.600000381469727,
                                   '2023-11-14 05:00:00': 22.65999984741211, '2023-11-15 05:00:00': 23.030000686645508,
                                   '2023-11-16 05:00:00': 23.3799991607666, '2023-11-17 05:00:00': 23.139999389648438,
                                   '2023-11-20 05:00:00': 23.309999465942383,
                                   '2023-11-21 05:00:00': 23.420000076293945}},
        'ABEA.F': {'currency': 'EUR', 'exchange': 'FRA', 'lastPrice': 125.54000091552734, 'timezone': 'Europe/Berlin',
                   'daily_info': {'2023-10-22 22:00:00': 128.75999450683594, '2023-10-23 22:00:00': 131.05999755859375,
                                  '2023-10-24 22:00:00': 119.0199966430664, '2023-10-25 22:00:00': 115.95999908447266,
                                  '2023-10-26 22:00:00': 115.13999938964844, '2023-10-29 23:00:00': 117.4000015258789,
                                  '2023-10-30 23:00:00': 116.94000244140625, '2023-10-31 23:00:00': 119.5,
                                  '2023-11-01 23:00:00': 120.16000366210938, '2023-11-02 23:00:00': 120.16000366210938,
                                  '2023-11-05 23:00:00': 121.26000213623047, '2023-11-06 23:00:00': 122.95999908447266,
                                  '2023-11-07 23:00:00': 122.66000366210938, '2023-11-08 23:00:00': 122.0999984741211,
                                  '2023-11-09 23:00:00': 124.0999984741211, '2023-11-12 23:00:00': 123.83999633789062,
                                  '2023-11-13 23:00:00': 123.41999816894531, '2023-11-14 23:00:00': 124.0,
                                  '2023-11-15 23:00:00': 126.26000213623047, '2023-11-16 23:00:00': 123.76000213623047,
                                  '2023-11-19 23:00:00': 124.4800033569336, '2023-11-20 23:00:00': 125.5,
                                  '2023-11-21 23:00:00': 125.54000091552734}}}

    @classmethod
    def setUpClass(cls):
        with open("test_companies_info.json", "r") as json_file:
            cls.__library_manager = json.load(json_file)

        cls.__tickers_list = ["GOOG", "GOOGL", "ABEA.DE", "GOOG.NE", "ABEA.F"]
        cls.__ticker_fetcher = TickerFetcher()
        cls.__data_processor = TickerDataProcessor()
        cls.__collected_info = {}

    def test_initialization(self):
        test_ticker = "goog"
        fetch_data_instance = FetchData(test_ticker)
        self.assertEqual(fetch_data_instance.ticker_to_search, "GOOG", "Ticker should be converted to uppercase")
