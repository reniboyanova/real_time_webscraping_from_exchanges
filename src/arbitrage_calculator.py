import logging
from itertools import combinations

from forex_python.converter import RatesNotAvailableError

from src.conversion_rate_calculator import ConversionRateCalculator

logging.basicConfig(level=logging.INFO, filename="app.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
class ArbitrageCalculator:
    """
    This class makes a calculation of arbitrage opportunities with providing data.
    It uses a dictionary with already collected data, and the list with tickers.
    The ArbitrageCalculator class also uses helper function
    """

    def __init__(self, collected_data, list_with_tickers):
        self.__collected_data = collected_data
        self.__list_with_tickers = list_with_tickers
        self.__rate_calculator = ConversionRateCalculator()

    def add_arbitrage_opportunities(self):
        """
        Add arbitrage opportunities by calculating by making pair between all tickers.
        For example self.list_with_tickers = ['TSLA', 'TSLA.NE', 'TL0.DE']
        ---> [('TSLA', 'TSLA.NE'), ('TSLA', 'TL0.DE'), ('TSLA.NE', 'TL0.DE')]
        Function looping thought the pairs and add to collection dictionary arbitrage opportunities between all pairs.
        The function uses another helping function self.____calculate_arbitrage_opportunities

        :return:
        """
        try:
            ticker_pairs = list(combinations(self.__list_with_tickers, 2))
            for ticker1, ticker2 in ticker_pairs:
                if ticker1 not in self.__collected_data or ticker2 not in self.__collected_data:
                    continue

                for time in self.__collected_data[ticker1]['daily_info']:
                    if time in self.__collected_data[ticker2]['daily_info']:
                        currency_1 = self.__collected_data[ticker1]['currency']
                        currency_2 = self.__collected_data[ticker2]['currency']

                        price_diff_1, price_diff_2 = self.__calculate_arbitrage_opportunities(time, ticker1, ticker2)

                        self.__collected_data[ticker1].setdefault(f'difference_in_{currency_2}_{ticker2}', {})[
                            time] = price_diff_1

                        self.__collected_data[ticker2].setdefault(f'difference_in_{currency_1}_{ticker1}', {})[
                            time] = price_diff_2
        except ValueError as e:
            logging.error(f"An error occurred: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def __calculate_arbitrage_opportunities(self, time, ticker1, ticker2):
        """
        Function takes two tickers from one pair, and time, witch needs to be same for both tickers.
        Makes calculations by using helping function self.__calculate_arbitrage
        :param time: time in string format (20.11.2023 14:30:00)
        :param ticker1: ticker symbol, for example, 'TSLA'
        :param ticker2: ticker symbol, for example, 'TL0.DE'
        :return:
        """
        try:
            price1 = self.__collected_data[ticker1]['daily_info'][time]
            price2 = self.__collected_data[ticker2]['daily_info'][time]
            currency_1 = self.__collected_data[ticker1]['currency']
            currency_2 = self.__collected_data[ticker2]['currency']
            date = time.split(' ')[0]

            arbitrage_1 = self.__calculate_arbitrage(price1, currency_1, price2, currency_2, date)
            arbitrage_2 = self.__calculate_arbitrage(price2, currency_2, price1, currency_1, date)

            price_diff_1 = str(arbitrage_1) + f' {currency_2}'
            price_diff_2 = str(arbitrage_2) + f' {currency_1}'

            return price_diff_1, price_diff_2
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

    def __calculate_arbitrage(self, price1, currency1, price2, currency2, date):
        """
        By using self.__get_conversion_rate_on_date it calculates the current date rate.
        :param price1: floating point number, for example, 123.456
        :param currency1: currency symbol in string 'USD'
        :param price2:  floating point number, for example, 125.678
        :param currency2: currency symbol in string 'CAD'
        :param date: date in string format - '2023-11-21'
        :return: calculated opportunity (floating point number)
        """
        try:
            conversion_rate = self.__rate_calculator.get_conversion_rate_on_date(currency2, currency1, date)
            converted_price2 = price2 * conversion_rate

            arbitrage_opportunity = converted_price2 - price1
            return arbitrage_opportunity
        except RatesNotAvailableError as e:
            logging.error(f"Rates Not Available error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during arbitrage calculation: {e}")
            return None

