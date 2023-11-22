import unittest
from datetime import datetime
from src.conversion_rate_calculator import ConversionRateCalculator
from forex_python.converter import RatesNotAvailableError


class TestConversionRateCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = ConversionRateCalculator()

    def test_rate_retrieval_with_valid_date(self):
        date = datetime.now().strftime('%Y-%m-%d')
        try:
            rate = self.calculator.get_conversion_rate_on_date('USD', 'CAD', date)
            self.assertIsInstance(rate, float)
        except RatesNotAvailableError:
            self.fail("RatesNotAvailableError raised unexpectedly!")

    def test_rate_retrieval_with_invalid_date(self):
        with self.assertRaises(ValueError):
            self.calculator.get_conversion_rate_on_date('USD', 'CAD', 'invalid-date')

    def test_rate_retrieval_with_invalid_currency(self):
        date = datetime.now().strftime('%Y-%m-%d')
        rate = self.calculator.get_conversion_rate_on_date('XXX', 'CAD', date)
        self.assertIsNone(rate, "Expected None for invalid currency code")
