from unittest import TestCase
from filer_data import DataFilter


class TestDataFilter(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_data = {
            "TickerA": {"daily_info": {"09:00": 100, "10:00": 105}},
            "TickerB": {"daily_info": {"09:00": 200, "10:00": 205, "11:00": 210}},
            "TickerC": {"daily_info": {}}
        }

    def test_longest_daily_info_determination(self):
        data_filter = DataFilter(self.sample_data)
        data_filter.filter_based_on_longest_daily_info()
        longest = max(self.sample_data, key=lambda ticker: len(self.sample_data[ticker]['daily_info']))
        self.assertEqual(longest, "TickerB", "TickerB should have the longest daily info")

    def test_filtering_of_other_tickers(self):
        data_filter = DataFilter(self.sample_data)
        data_filter.filter_based_on_longest_daily_info()
        for ticker, info in self.sample_data.items():
            if ticker != "TickerB":
                for time in info['daily_info']:
                    self.assertIn(time, self.sample_data["TickerB"]['daily_info'],
                                  f"{time} should be in TickerB's daily info")

    def test_no_change_for_longest_ticker_info(self):
        original_data = self.sample_data["TickerB"]['daily_info'].copy()
        data_filter = DataFilter(self.sample_data)
        data_filter.filter_based_on_longest_daily_info()
        self.assertEqual(self.sample_data["TickerB"]['daily_info'], original_data,
                         "TickerB's daily info should remain unchanged")

    def test_handling_empty_data(self):
        empty_data_filter = DataFilter({"TickerD": {"daily_info": {}}})
        empty_data_filter.filter_based_on_longest_daily_info()
        self.assertEqual(empty_data_filter.collected_data, {"TickerD": {"daily_info": {}}},
                         "Empty data should remain unchanged")