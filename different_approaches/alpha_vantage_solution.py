from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import requests


def get_api_key(filepath):
    with open(filepath, 'r') as file:
        return file.read().strip()

api_key = get_api_key('../scraper_module/alpha_api.txt')
ts = TimeSeries(key=api_key, output_format='pandas')

# first step:
# after that make it in class (object)

def find_most_actives(key):
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={key}'
    response = requests.get(url)
    data = response.json()

    most_actives = {ticker['ticker']: [] for ticker in data['most_actively_traded']}

    return most_actives

most_act = find_most_actives(api_key)

# step 2:
# find bestMatches

def find_best_matches(list_with_tickers: dict):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey={api_key}"
    for ticker in list_with_tickers:
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": ticker,
            "apikey": api_key,
            "datatype": "json"
        }

        response = requests.get(url, params=params)
        data = response.json()

        for match in data['bestMatches']:
            info = {
                'symbol': match.get('1. symbol', ''),
                'name': match.get('2. name', ''),
                'timezone': match.get('7. timezone', ''),
                'currency': match.get('8. currency', '')
            }
            print(info)
            most_act[ticker].append(info)

# OK Step 3:
# Here we will check the dayly info
def get_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data.get("Global Quote")


# symbols = ["TSLA", "TL0.DE", "TSLA.CB"]
# lufax = ['LU', '6623.HK', '6V3.F', '6V3.DU', '6V3.MU', '6V3.BE']
#
# for symbol in symbols:
#     stock_data = get_stock_data(symbol, api_key)
#     if stock_data:
#         print(f"{symbol}: {stock_data}")
#     else:
#         print(f"No data available for {symbol}")

 # Replace with your Alpha Vantage API key
KEYWORDS = "The Gap"    # Replace with your search keywords

# Setting up the API URL and parameters


url2 = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey={api_key}'
r = requests.get(url2)
data2 = r.json()

print(data2)

# https://finance.yahoo.com/quote/TSLA.NE?p=TSLA.NE&.tsrc=fin-srch
# https://finance.yahoo.com/quote/TSLA?p=TSLA&.tsrc=fin-srch
# https://finance.yahoo.com/quote/TL0.DE?p=TL0.DE&.tsrc=fin-srch
# f"https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"

# Multitreading

