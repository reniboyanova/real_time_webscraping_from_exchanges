from unittest import TestCase
import json

from src.arbitrage_calculator import ArbitrageCalculator
from itertools import combinations


class TestArbitrageCalculator(TestCase):
    test_data = None
    test_list = None
    arb_calculator_test = None

    @classmethod
    def setUpClass(cls):
        with open("test_data.json", "r") as json_file:
            cls.test_data = json.load(json_file)

        cls.test_list = [ticker for ticker in cls.test_data.keys()]
        cls.arb_calculator_test = ArbitrageCalculator(cls.test_data, cls.test_list)

    def test_initialisation(self):
        self.assertEqual(self.arb_calculator_test.__collected_data, self.test_data)
        self.assertEqual(self.arb_calculator_test.__list_with_tickers, self.test_list)

    def test_ticker_pair_generation(self):
        expected_pairs = [('MSFT', 'MSFT.MX')]
        result = list(combinations(self.test_data, 2))
        self.assertEqual(result, expected_pairs)

    def test_arbitrage_calculator(self):
        time = "2023-11-21 16:30:00"
        ticker1, ticker2 = 'MSFT', 'MSFT.MX'
        """
        Here using name mangling to use __calculate_arbitrage_opportunities()
        """
        price_diff_1, price_diff_2 = self.arb_calculator_test._ArbitrageCalculator__calculate_arbitrage_opportunities(
            time, ticker1, ticker2)

        expected_value_1 = "1.5157819246557551 MXN"
        expected_value_2 = "-26.077527846897283 USD"

        self.assertEqual(expected_value_1, price_diff_1)
        self.assertEqual(expected_value_2, price_diff_2)

    def test_arbitrage_for_non_existing_time(self):
        non_existing_time = "2023-11-22 14:30:00"
        ticker1, ticker2 = 'MSFT', 'MSFT.MX'
        self.arb_calculator_test.add_arbitrage_opportunities()
        self.assertNotIn(non_existing_time, self.arb_calculator_test._ArbitrageCalculator__collected_data[ticker1])
        self.assertNotIn(non_existing_time, self.arb_calculator_test._ArbitrageCalculator__collected_data[ticker2])

    def test_arbitrage_with_invalid_currency(self):
        self.arb_calculator_test._ArbitrageCalculator__list_with_tickers.append('INVALID')
        self.arb_calculator_test.add_arbitrage_opportunities()
        self.assertNotIn('INVALID', self.arb_calculator_test._ArbitrageCalculator__list_with_tickers)

