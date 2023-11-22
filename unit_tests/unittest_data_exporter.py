import unittest
import pandas as pd
from data_exporter import DataExporter

class TestDataExporter(unittest.TestCase):

    def test_create_dataframe_with_valid_input(self):
        input_data = {
            "Col_1": [1, 2, 3],
            "Col_2": [4, 5]
        }
        result = DataExporter.create_dataframe(input_data)
        expected_output = pd.DataFrame({
            "Col_1": [1, 2, 3],
            "Col_2": [4, 5, '']
        })
        pd.testing.assert_frame_equal(result, expected_output)

    def test_create_dataframe_with_mixed_input(self):
        input_data = {
            "Col_1": [1, 2, 3],
            "Col_2": "Hello! I am test!"
        }
        result = DataExporter.create_dataframe(input_data)
        expected_output = pd.DataFrame({
            "Col_1": [1, 2, 3],
            "Col_2": ["Hello! I am test!", "Hello! I am test!", "Hello! I am test!"]
        })
        pd.testing.assert_frame_equal(result, expected_output)

    def test_create_dataframe_with_empty_dictionary(self):
        input_data = {}
        result = DataExporter.create_dataframe(input_data)
        expected_output = pd.DataFrame({})
        pd.testing.assert_frame_equal(result, expected_output)

    def test_create_dataframe_with_non_dictionary_input(self):
        input_data = "I am not a dictionary!"
        with self.assertRaises(TypeError):
            DataExporter.create_dataframe(input_data)

