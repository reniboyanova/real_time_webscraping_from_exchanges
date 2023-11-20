import requests
from bs4 import BeautifulSoup
import json

from forex_python.converter import CurrencyRates

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency)
    return rate

exchange_rate = get_exchange_rate('USD', 'JPY')
print(f"Exchange Rate from USD to JPY: {exchange_rate}")

def make_soup(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def scrape_listed_stocks_data(url: str) -> dict:
    most_actives_tickers = {}
    soup = make_soup(url)
    table_body = soup.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        link = row.find('a', {'data-test': 'quoteLink'})
        price = row.find('fin-streamer').get('value')
        if link and price:
            symbol = link.text
            link_href = "https://finance.yahoo.com" + link['href']
            most_actives_tickers[symbol] = {'url': link_href, 'price': float(price)}
    return most_actives_tickers

def scrape_search_bar_info(url: str):
    """
    <li role="option" title="Tesla, Inc." tabindex="0" data-type="quotes" data-id="result-quotes-0" data-test="srch-sym" data-index="0" data-pindex="1" class="modules_linkItem__P-S-4 modules_quoteItem__Ri1wp modules_selectedBackground__-Eg6s">
    <div class="modules_quoteLeftCol__gkCSv modules_Ell__77DLP modules_IbBox__2pmLe"><div class="modules_quoteSymbol__hpPcM">TSLA</div><div class="modules_quoteCompanyName__YUC7Y modules_Ell__77DLP">
    <strong>Tesla</strong>, Inc.</div></div>
    <div class="modules_quoteRightCol__xPEOm">
    <span class="modules_quoteSpan__FveMi">Equity - NMS</span></div></li>
    """

def json_dumps(data: dict):
    json_data = json.dumps(data, indent=4)

    with open('scraper_module/most_active_stocks.json', 'w') as file:
        file.write(json_data)


if __name__ == "__main__":
    active_stocks = scrape_listed_stocks_data('https://finance.yahoo.com/most-active/')
    print(active_stocks)