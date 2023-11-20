import json
from datetime import datetime

import pytz
import yfinance as yf
from forex_python.converter import CurrencyRates

dict_with_info = {}


def convert_to_utc_time(time_str, date_str, current_tz_str):
    current_tz = pytz.timezone(current_tz_str)
    utc_tz = pytz.timezone('UTC')

    current_time = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M:%S')

    current_time = current_tz.localize(current_time)
    utc_time = current_time.astimezone(utc_tz)

    return utc_time.strftime('%Y-%m-%d %H:%M:%S')


def get_ticker_info(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.fast_info

    if ticker_symbol not in dict_with_info:

        info_to_add = {
            'currency': info.get('currency'),
            'exchange': info.get('exchange'),
            'lastPrice': info.get('lastPrice'),
            'timezone': info.get('timezone')
        }
        dict_with_info[ticker_symbol] = info_to_add

        historical_data = ticker.history(period='1d', interval='30m')
        formatted_historical_data = {}
        for index, row in historical_data.iterrows():
            date_str = str(index.date())
            time_str = str(index.time())  # Получаване на времето от историческите данни
            utc_time = convert_to_utc_time(time_str, date_str, dict_with_info[ticker_symbol]['timezone'])

            close_value = row['Close']
            formatted_historical_data[utc_time] = close_value

        dict_with_info[ticker_symbol]['daily_info'] = formatted_historical_data


# for ticker_ind in ['AMZN', 'AMZN.MX', 'AMZ.DE']:
#     print('__________________________new line_____________________________\n')
#     get_ticker_info(ticker_ind)
#
# print(dict_with_info)

my_info = {
    'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125, 'timezone': 'America/New_York',
             'daily_info': {'2023-11-17 14:30:00': 143.9600067138672, '2023-11-17 15:00:00': 144.55999755859375,
                            '2023-11-17 15:30:00': 144.36219787597656, '2023-11-17 16:00:00': 144.20010375976562,
                            '2023-11-17 16:30:00': 144.1002960205078, '2023-11-17 17:00:00': 144.3000030517578,
                            '2023-11-17 17:30:00': 144.58999633789062, '2023-11-17 18:00:00': 144.7133026123047,
                            '2023-11-17 18:30:00': 144.67019653320312, '2023-11-17 19:00:00': 144.74000549316406,
                            '2023-11-17 19:30:00': 144.43499755859375, '2023-11-17 20:00:00': 144.56500244140625,
                            '2023-11-17 20:30:00': 145.17999267578125}},
    'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125, 'timezone': 'America/Mexico_City',
                'daily_info': {'2023-11-17 14:30:00': 2478.0, '2023-11-17 15:00:00': 2484.5,
                               '2023-11-17 15:30:00': 2478.5, '2023-11-17 16:00:00': 2482.030029296875,
                               '2023-11-17 17:00:00': 2485.0, '2023-11-17 17:30:00': 2485.0,
                               '2023-11-17 18:00:00': 2490.0, '2023-11-17 18:30:00': 2490.0,
                               '2023-11-17 19:00:00': 2493.6298828125, '2023-11-17 19:30:00': 2487.840087890625}},
    'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.66000366210938, 'timezone': 'Europe/Berlin',
               'daily_info': {'2023-11-17 08:00:00': 132.4199981689453, '2023-11-17 08:30:00': 132.3000030517578,
                              '2023-11-17 09:00:00': 132.05999755859375, '2023-11-17 09:30:00': 132.32000732421875,
                              '2023-11-17 10:00:00': 132.1999969482422, '2023-11-17 10:30:00': 132.25999450683594,
                              '2023-11-17 11:00:00': 132.13999938964844, '2023-11-17 11:30:00': 132.22000122070312,
                              '2023-11-17 12:00:00': 132.05999755859375, '2023-11-17 12:30:00': 132.0800018310547,
                              '2023-11-17 13:00:00': 132.17999267578125, '2023-11-17 13:30:00': 131.5,
                              '2023-11-17 14:00:00': 131.36000061035156, '2023-11-17 14:30:00': 132.36000061035156,
                              '2023-11-17 15:00:00': 132.77999877929688, '2023-11-17 15:30:00': 132.63999938964844,
                              '2023-11-17 16:00:00': 132.52000427246094}}}


def filter_common_daily_info(dict_with_info):
    all_timestamps = [set(info['daily_info'].keys()) for info in dict_with_info.values()]

    common_timestamps = set.intersection(*all_timestamps)
    print(common_timestamps)
    for ticker, info in dict_with_info.items():
        filtered_daily_info = {time: value for time, value in info['daily_info'].items() if time in common_timestamps}
        dict_with_info[ticker]['daily_info'] = filtered_daily_info

    return dict_with_info


def take_currency(dict_with_info):
    currency_rates_set = set()
    for ticker, ticker_info in dict_with_info.items():
        currency_rates_set.add(ticker_info['currency'])

    return currency_rates_set


def convert_currency(from_currency, to_currency, amount, date_str):
    c = CurrencyRates()
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    rate = c.get_rate(from_currency, to_currency, date_obj)

    converted_amount = rate * amount
    print(f"convert from {from_currency} to {to_currency} - {amount} = {converted_amount}")
    return converted_amount


currensies = take_currency(my_info)

from itertools import combinations


def calculate_arbitrage(dict_with_info):
    tickers = list(dict_with_info.keys())
    ticker_pairs = list(combinations(tickers, 2))

    for pair in ticker_pairs:
        ticker1, ticker2 = pair
        print(ticker1, ticker2)
        for time in dict_with_info[ticker1]['daily_info']:
            if time in dict_with_info[ticker2]['daily_info']:
                price1 = dict_with_info[ticker1]['daily_info'][time]
                price2 = dict_with_info[ticker2]['daily_info'][time]
                currency_1 = dict_with_info[ticker1]['currency']
                currency_2 = dict_with_info[ticker2]['currency']
                date = time.split(' ')[0]

                converted_price1 = convert_currency(currency_2, currency_1, price2, date)
                converted_price2 = convert_currency(currency_1, currency_2, price1, date)

                # Just to be easier, I made it str to add currency
                price_diff_1 = str(converted_price1 - price1) + f' {currency_1}'
                price_diff_2 = str(converted_price2 - price2) + f' {currency_2}'

                dict_with_info[ticker1].setdefault(f'difference_in_{currency_1}_{ticker2}', {})[time] = price_diff_1

                dict_with_info[ticker2].setdefault(f'difference_in_{currency_2}_{ticker1}', {})[time] = price_diff_2

    return dict_with_info


filtered_info = filter_common_daily_info(my_info)
# print(filtered_info)

filtered_info_dict = {
    'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125, 'timezone': 'America/New_York',
             'daily_info': {'2023-11-17 14:30:00': 143.9600067138672, '2023-11-17 15:00:00': 144.55999755859375,
                            '2023-11-17 15:30:00': 144.36219787597656, '2023-11-17 16:00:00': 144.20010375976562}},
    'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125, 'timezone': 'America/Mexico_City',
                'daily_info': {'2023-11-17 14:30:00': 2478.0, '2023-11-17 15:00:00': 2484.5,
                               '2023-11-17 15:30:00': 2478.5, '2023-11-17 16:00:00': 2482.030029296875}},
    'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.66000366210938, 'timezone': 'Europe/Berlin',
               'daily_info': {'2023-11-17 14:30:00': 132.36000061035156, '2023-11-17 15:00:00': 132.77999877929688,
                              '2023-11-17 15:30:00': 132.63999938964844, '2023-11-17 16:00:00': 132.52000427246094}}}

print(calculate_arbitrage(filtered_info_dict))

last_dict = {
    'AMZN': {'currency': 'USD', 'exchange': 'NMS', 'lastPrice': 145.17999267578125, 'timezone': 'America/New_York',
             'daily_info': {'2023-11-17 14:30:00': 143.9600067138672, '2023-11-17 15:00:00': 144.55999755859375,
                            '2023-11-17 15:30:00': 144.36219787597656, '2023-11-17 16:00:00': 144.20010375976562},
             'difference_in_MXN_AMZN.MX': {'2023-11-17 14:30:00': '0.076177672527308 USD',
                                           '2023-11-17 15:00:00': '-0.14599428660136482 USD',
                                           '2023-11-17 15:30:00': '-0.2969504983822162 USD',
                                           '2023-11-17 16:00:00': '0.07033003860919962 USD'},
             'difference_in_EUR_AMZ.DE': {'2023-11-17 14:30:00': '-0.1111580505371137 USD',
                                          '2023-11-17 15:00:00': '-0.2546948852539117 USD',
                                          '2023-11-17 15:30:00': '-0.20904653930665518 USD',
                                          '2023-11-17 16:00:00': '-0.1773631164550693 USD'}},
    'AMZN.MX': {'currency': 'MXN', 'exchange': 'MEX', 'lastPrice': 2495.550048828125, 'timezone': 'America/Mexico_City',
                'daily_info': {'2023-11-17 14:30:00': 2478.0, '2023-11-17 15:00:00': 2484.5,
                               '2023-11-17 15:30:00': 2478.5, '2023-11-17 16:00:00': 2482.030029296875},
                'difference_in_USD_AMZN': {'2023-11-17 14:30:00': '17.841047572703246 MXN',
                                           '2023-11-17 15:00:00': '21.743115567967834 MXN',
                                           '2023-11-17 15:30:00': '24.313853661540634 MXN',
                                           '2023-11-17 16:00:00': '17.97359145315022 MXN'},
                'difference_in_EUR_AMZ.DE': {'2023-11-17 14:30:00': '2.8896714401248573 MXN',
                                             '2023-11-17 15:00:00': '4.261907119750958 MXN',
                                             '2023-11-17 15:30:00': '7.637828559875743 MXN',
                                             '2023-11-17 16:00:00': '1.8586707839967858 MXN'}},
    'AMZ.DE': {'currency': 'EUR', 'exchange': 'GER', 'lastPrice': 132.66000366210938, 'timezone': 'Europe/Berlin',
               'daily_info': {'2023-11-17 14:30:00': 132.36000061035156, '2023-11-17 15:00:00': 132.77999877929688,
                              '2023-11-17 15:30:00': 132.63999938964844, '2023-11-17 16:00:00': 132.52000427246094},
               'difference_in_USD_AMZN': {'2023-11-17 14:30:00': '0.10228013483356335 EUR',
                                          '2023-11-17 15:00:00': '0.23435304127153245 EUR',
                                          '2023-11-17 15:30:00': '0.19235051463621744 EUR',
                                          '2023-11-17 16:00:00': '0.16319756758841208 EUR'},
               'difference_in_MXN_AMZN.MX': {'2023-11-17 14:30:00': '-0.15416925548188942 EUR',
                                             '2023-11-17 15:00:00': '-0.22738053830667582 EUR',
                                             '2023-11-17 15:30:00': '-0.4074921204617965 EUR',
                                             '2023-11-17 16:00:00': '-0.09916348515469053 EUR'}}}

with open('stock_data.json', 'w') as file:
    json.dump(last_dict, file, indent=4)
# my 2 func for convert time:

# def convert_to_ny_time(time_str):
#     symbol_to_split = '-' if '-' in time_str else '+'
#     current_time, difference = time_str.split(symbol_to_split)
#     hours, minutes, seconds = map(int, current_time.split(':'))
#     diff_hours, diff_minutes = map(int, difference.split(':'))
#
#     if symbol_to_split == '-':
#         new_hours = hours - diff_hours
#         new_minutes = minutes - diff_minutes
#     else:
#         new_hours = hours + diff_hours
#         new_minutes = minutes + diff_minutes
#
#     if new_minutes < 0:
#         new_hours -= 1
#         new_minutes += 60
#     elif new_minutes >= 60:
#         new_hours += 1
#         new_minutes -= 60
#
#     if new_hours < 0:
#         new_hours += 24
#     elif new_hours >= 24:
#         new_hours -= 24
#
#     new_time = f'{new_hours:02d}:{new_minutes:02d}:{seconds:02d}'
#     return new_time
#
# print(convert_to_ny_time('02:30:00-06:00'))
