import json
from datetime import datetime

from forex_python.converter import CurrencyRates

tesla = ['TSLA', 'TSLA.NE', 'TL0.DE']
lufax = ['LU', '6623.HK', '6V3.F', '6V3.DU', '6V3.MU', '6V3.BE']
palantir = ['PLTR', 'PLTR.VI', 'PTX.DE', 'PTX.F']
nu_holdings = ['NU',
               'ROXO34.SA',
               'NU.CL', 'NUN.MX', 'M1Z.SG', 'M1Z.MU']

plug_power = ['PLUG', 'PLUN.F', 'PLUN.DE', 'PLUG.MX', 'PLUN.SG', '0R1J.IL']
amazon = ['AMZN', 'AMZN.MX', 'AMZ.DE', 'AMZN.NE', 'AMZO34.SA', 'AMZN.BA']

marathon_digital = ['MARA', 'MARA.MX', 'M44.MU', 'US5657881067.SG', 'M44.F']

alibaba = ['BABA', '9988.HK', 'AHLA.DE', 'AHLA.VI', 'BABAF', 'BABAN.MX']

cisco_systems = ['CSCO', 'CSCO.MX', 'CSCO.NE', 'CSCO.BA', 'CIS.DE', 'CIS.BE']
macy_s = ['M', 'MACY.VI', 'M.MX', 'FDO.DE', 'FDO.DU']
# to check if html address existing

# to search by name and  scrape info after get name. Then start paralel searching and calculating
# make tuples and check how to make it library

# Multitreading
# to take currency, bid price, and compare with ask price of the others markets;
# to make error handling; to make currency converter by the token currencies;
# to export in csv or google sheets
# checking for valid url, if not make a message
# make a frame - gui?


"""
# stocks.py
class StockSymbols:
    def __init__(self):
        self.symbols = {
            'tesla': ['TSLA', 'TSLA.NE', 'TSLA.NE'],
            'lufax': ['LU', '6623.HK', '6V3.F', '6V3.DU', '6V3.MU', '6V3.BE'],
            'palantir': ['PLTR', 'PLTR.VI', 'PTX.DE', 'PTX.F'],
        
        }

    def get_symbols(self, company):
        return self.symbols.get(company.lower())

import py_compile
py_compile.compile('stocks.py')

from stocks import StockSymbols

stock_library = StockSymbols()
tesla_symbols = stock_library.get_symbols('tesla')
print(tesla_symbols)
"""
#
#
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

def make_soup(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def make_url(symbol):
    return f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch"


info_for_companies = []
def save_to_json_file(data, filename="company_data.json"):
    """
    Saves the given data to a JSON file.

    :param data: The data to be saved.
    :param filename: The name of the file to save the data in.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def scrape_single_page_info(company_symbol):
    company_info = {}
    current_url = make_url(company_symbol)
    # current_url = 'https://finance.yahoo.com/quote/INTC?p=INTC'
    soup = make_soup(current_url)
    # time.sleep(15)
    company_name = soup.find('h1').text.split(f' ({company_symbol})')[0]
    # print(company_name)
    exchange, currency = '', ''
    element_div = soup.find('div', {'class': 'C($tertiaryColor) Fz(12px)'})
    if element_div:
        element_text = element_div.text
        exchange, currency = element_text.split(' - ')[0], element_text.split(' in ')[-1]
        time.sleep(10)
    else:
        exchange, currency = 'Unknown', 'Unknown'

    # exchange, currency = element.split(' - ')[0], element.split(' in ')[-1]
    # print(currency)
    # print(exchange)
    # good to here!
    # time.sleep(15)
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    bid_value = 0
    ask_value = 0
    for row in rows:
        time.sleep(5)
        cells = row.find_all('td')
        if cells[0].text.strip() == 'Bid':
            bid_value = cells[1].text.split(' x ')[0]
            # print(bid_value)
        elif cells[0].text.strip() == 'Ask':
            ask_value = cells[1].text.split(' x ')[0]
            # print(ask_value)
    company_info[company_symbol] = {'Full Company Name': company_name if company_name else '',
                                    'Currency': currency if currency else '',
                                    'Stock Market': exchange if exchange else '',
                                    'Bid': float(bid_value) if bid_value != 0 else '',
                                    'Ask': float(ask_value) if ask_value != 0 else ''}

    save_to_json_file(company_info)

scrape_single_page_info('TSLA.NE')

# scrape_single_page_info('PLTR')
# print(info_for_companies)

# def fetch_info_for_symbols(symbols):
#     info_for_companies = []

#     with ThreadPoolExecutor(max_workers=4) as executor:
#         futures = [executor.submit(scrape_single_page_info, symbol) for symbol in symbols]
#         i = 0
#         for future in futures:
#             i+=1
#             info_for_companies.append(future.result())
#             print(i)
#     return info_for_companies
#
#
# palantir2 = ['PLTR', 'PLTR.VI', 'PTX.DE', 'PTX.F']
# all_info = fetch_info_for_symbols(palantir2)
# print(all_info)
#https://finance.yahoo.com/quote/PTX.F?p=PTX.F&.tsrc=fin-srch


# import yfinance as yf
# from forex_python.converter import CurrencyRates
#
#
# data = yf.download("6623.HK", period="1d", interval='1m')
# data2 = yf.download("LU", period="1d", interval='1m')
# print(data)
# print(data2)
#
# ticker2 = yf.Ticker("6623.HK")
# info2 = ticker2.fast_info
# period_info = ticker2.history(period="1d", interval='1m')
# currency2 = info2.get('currency')
# print(f"Currency for 6623.HK: {currency2}")
# print(period_info)

# def convert_currency(amount, from_currency, to_currency):
#     converter = CurrencyRates()
#     converted_amount = converter.convert(from_currency, to_currency, amount)
#     return converted_amount
#
# converted_amount = convert_currency(0.92, 'HKD', 'USD')
# profit = 15.54 - converted_amount
# print(profit)

#
# import yfinance as yf

#
# lufax_2 = ['LU', '6623.HK', '6V3.F', '6V3.DU', '6V3.MU', '6V3.BE']
# def collect_data_for_tickers(tickers: list, start_date, end_date) -> dict:
#     collected_data = {}
#     for ticker in tickers:
#         current_ticker_info = yf.Ticker(ticker)
#         info = current_ticker_info.fast_info
#         currency = info.get('currency') if info.get('currency') else 'N/A'
#
#         ticker_data = yf.download(ticker, start=start_date, end=end_date)
#         close_prices = ticker_data['Close'].iloc[-1] if not ticker_data['Close'].empty else 0
#
#         collected_data[ticker] = {'currency': currency, 'data': close_prices}
#
#     return collected_data
#
# start_date_str = input("Enter the start date (YYYY-MM-DD): ")
# end_date_str = input("Enter the end date (YYYY-MM-DD): ")
# start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
# end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
#
# my_data = collect_data_for_tickers(lufax_2, start_date, end_date)
#
#
# def convert_currency(from_currency, to_currency, amount):
#     converter = CurrencyRates()
#     converted_amount = converter.convert(from_currency, to_currency, amount)
#     return converted_amount
#
#
# for ticker, data in my_data.items():
#     PRIME_CONVERT_CURRENCY = 'USD'
#     currency_to_convert = my_data[ticker]['currency']
#     close_price = my_data[ticker]['data']
#     if currency_to_convert != PRIME_CONVERT_CURRENCY:
#         my_data[ticker]['converted_data'] = convert_currency(currency_to_convert, PRIME_CONVERT_CURRENCY, close_price)
#     else:
#         my_data[ticker]['converted_data'] = close_price
#
# arbitrage_profit_info = {}
#
# for ticker, data in my_data.items():
#     compare_price = my_data[ticker]['converted_data']
#     for ticker_to_compare, data_to_compare in my_data.items():
#         current_price_to_compare = my_data[ticker_to_compare]['converted_data']
#
#         if abs(compare_price - current_price_to_compare) >= 1:
#             arbitrage_profit_info[ticker] = {'ticker_to_compare': ticker_to_compare,
#                                              'profit': abs(compare_price - current_price_to_compare),
#                                              'price_of_ticker': compare_price,
#                                              'price_of_ticker_2': current_price_to_compare}
#
# print(arbitrage_profit_info)
