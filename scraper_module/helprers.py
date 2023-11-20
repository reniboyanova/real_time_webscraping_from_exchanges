import json
from datetime import datetime
import pytz
from forex_python.converter import CurrencyRates


def get_api_key(filepath):
    """
    Helping function to open safety file with API key
    :param filepath: Real path to the file witch holds API key
    :return: string information (Key) from file
    """
    with open(filepath, 'r') as file:
        return file.read().strip()


def is_valid_timezone(time_zone):
    """
    Check if time_zone exist in the list with time zones in module pytz
    :param time_zone: time_zone in string ('UTC' - will be valid or 'Asia/Kolkata' - valid)
    :return: True or False
    """
    if not isinstance(time_zone, str):
        raise TypeError("Time zone need to be string!")

    return time_zone in pytz.all_timezones


def convert_to_utc_time(time_str, date_str, current_tz_str):
    """
    Convert any-time to UTC time
    :param time_str: Example - '12:00:00'
    :param date_str: Example - '2023-11-17'
    :param current_tz_str: Time zone in format 'Region/City', example - 'America/New_York'
    :return: converted time in UTC timezone (string)
    """
    if not is_valid_timezone(current_tz_str):
        raise ValueError(f"Invalid timezone: {current_tz_str}")

    try:
        current_tz = pytz.timezone(current_tz_str)
        utc_tz = pytz.timezone('UTC')

        current_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M:%S')

        current_time = current_tz.localize(current_time)
        utc_time = current_time.astimezone(utc_tz)

        return utc_time.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Error in parsing date or time: {e}")


def convert_currency(from_currency, to_currency, amount, date_str):
    c = CurrencyRates()
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    print(date_obj)
    rate = c.get_rate(from_currency, to_currency, date_obj)

    converted_amount = rate * amount
    print(f"convert from {from_currency} to {to_currency} - {amount} = {converted_amount}")
    return converted_amount


def record_in_json_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def prompt_user_to_paste_ticker():
    user_input = input("Insert ticker symbol or company name: ")
    return user_input


def prompt_user_to_paste_period_interval():
    user_period = input(
        "Insert period and period (example for valid periods 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max) : ")
    user_interval = input(
        "Insert period and interval (example for valid periods 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo) : ")
    return user_period, user_interval



if __name__ == "__main__":
    amound = 100
    currency1 = 'USD'
    currency2 = 'CAD'
    date_ = '2023-11-17'
    amound2 = 85

    print(convert_currency(currency1, currency2, amound, date_))
    print(convert_currency(currency2, currency1, amound2, date_))
