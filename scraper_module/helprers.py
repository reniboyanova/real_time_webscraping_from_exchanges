from datetime import datetime
import pytz

def get_api_key(filepath):
    """
    Helping function to open safety file with API key
    :param filepath: Real path to the file witch holds API key
    :return: string information (Key) from file
    """
    with open(filepath, 'r') as file:
        return file.read().strip()


current_time_to_check = '11:15:00'
time_zone_1 = 'US/Eastern'
time_zone_2 = 'CET'

def is_valid_timezone(time_zone):
    """
    Check if time_zone exist in the list with time zones in module pytz
    :param time_zone: time_zone in string ('UTC' - will be valid or 'Asia/Kolkata' - valid)
    :return: True or False
    """
    if not isinstance(time_zone, str):
        raise TypeError("Time zone need to be string!")

    return time_zone in pytz.all_timezones

def convert_time_zone(current_time, from_time_zone, to_time_zone):
    """
    Helping function to convert current time from one zone to another
    :param current_time: Time in string format HH:MM:SS
    :param from_time_zone: Name of time zone that we convert from (string)
    :param to_time_zone: Name of time zone that we convert to (string)
    :return: converted time in string
    """
    naive_datetime = datetime.strptime(current_time, '%H:%M:%S')
    print(naive_datetime)
    from_timezone = pytz.timezone(from_time_zone)
    print(from_timezone)
    from_aware_datetime = from_timezone.localize(naive_datetime)
    print(from_aware_datetime)
    to_timezone = pytz.timezone(to_time_zone)
    print(to_timezone)
    to_aware_datetime = from_aware_datetime.astimezone(to_timezone)
    print(to_aware_datetime)
    return to_aware_datetime.strftime('%H:%M:%S')


converted_time = convert_time_zone(current_time_to_check, time_zone_1, time_zone_2)
print('==============================')
print(converted_time)

