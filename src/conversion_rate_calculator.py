from datetime import datetime

from forex_python.converter import CurrencyRates, RatesNotAvailableError


class ConversionRateCalculator:
    @staticmethod
    def get_conversion_rate_on_date(base_currency, target_currency, date):
        """
        Calculate the concrete date currency rate, by using forex_python module and class CurrencyRates from it.
        Function also uses datetime.datetime (C module), to format date, and makes it date object from string
        :param base_currency: currency symbol in string 'USD'
        :param target_currency: currency symbol in string 'CAD'
        :param date: date in string format - '2023-11-21'
        :return: currency rate between base and target currency (float)
        """
        c = CurrencyRates()
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            rate = c.get_rate(base_currency, target_currency, date_obj)
            if rate is None:
                raise ValueError(f"Invalid currency code: {base_currency} or {target_currency}")
            return rate
        except RatesNotAvailableError:
            print(f"Not available rate for this date {date}")
