import unittest
from data_cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):

    def test_clean_data_with_valid_input(self):
        input_data = {
            "Ticker1": {"daily_info": [1, 2, 3]},
            "Ticker2": {"daily_info": []},
            "Ticker3": {"daily_info": [4, 5]}
        }
        expected_output = {
            "Ticker1": {"daily_info": [1, 2, 3]},
            "Ticker3": {"daily_info": [4, 5]}
        }
        result = DataCleaner.clean_data(input_data)
        self.assertEqual(result, expected_output)

    def test_clean_data_with_empty_dictionary(self):
        input_data = {}
        expected_output = {}
        result = DataCleaner.clean_data(input_data)
        self.assertEqual(result, expected_output)

    def test_clean_data_with_non_dictionary_input(self):
        input_data = "I'm not a dictionary!"
        with self.assertRaises(TypeError):
            DataCleaner.clean_data(input_data)