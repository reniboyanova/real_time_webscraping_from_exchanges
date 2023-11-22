import json
import logging
from datetime import datetime
import pytz
logging.basicConfig(level=logging.INFO, filename="app.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

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


def record_in_json_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def prompt_user_to_paste_ticker():
    while True:
        user_input = input("Insert ticker symbol or company name: ")
        if 1 <= len(user_input) <= 20:
            # Maybe using some library with all company names and tickers?
            return user_input
        print("Invalid ticker symbol, please try again")


def prompt_user_to_paste_period_interval():
    try:
        with open('period_interval_mapping.json', 'r') as file:
            valid_period_intervals = json.load(file)

        while True:
            user_period = input("Insert period (valid periods 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")
            user_interval = input("Insert interval (valid intervals based on your period): ")

            if user_period in valid_period_intervals and user_interval in valid_period_intervals[user_period]:
                return user_period, user_interval
            print("Invalid period and interval combination, please try again!")
    except FileNotFoundError as e:
        logging.error(f"File was not found {e}")
        print("Error: The required configuration file is missing. Please check your setup.")

