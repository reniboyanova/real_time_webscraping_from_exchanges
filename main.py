import re
import json

import csv
from io import StringIO

from bs4 import BeautifulSoup

import requests



"""
<tr class="simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor) ">
<td colspan="" class="Va(m) Ta(start) Pstart(6px) Pend(10px) Miw(90px) Start(0) Pend(10px) simpTblRow:h_Bgc($hoverBgColor)  Pos(st) Bgc($lv3BgColor) Z(1)  Bgc($lv2BgColor)  Ta(start)! Fz(s)" aria-label="Symbol"><label data-id="portfolio-checkbox" class="Ta(c) Pos(r) Va(tb) Pend(5px) D(n)--print ">
<input type="checkbox" class="Pos(a) Op(0) checkbox" aria-label="Select TSLA">
<svg class="Va(m)! H(16px) W(16px) checkbox:f+Stk($linkColor)! checkbox:f+Fill($linkColor)! Stk($plusGray) Fill($plusGray) Cur(p)" width="16" height="16" viewBox="0 0 24 24" data-icon="checkbox-unchecked" style="stroke-width: 0; vertical-align: bottom;">
<path d="M3 3h18v18H3V3zm19-2H2c-.553 0-1 .448-1 1v20c0 .552.447 1 1 1h20c.552 0 1-.448 1-1V2c0-.552-.448-1-1-1z">
</path></svg></label><a data-test="quoteLink" href="/quote/TSLA?p=TSLA" title="Tesla, Inc." class="Fw(600) C($linkColor)">TSLA</a><div class="W(3px) Pos(a) Start(100%) T(0) H(100%) Bg($pfColumnFakeShadowGradient) Pe(n) Pend(5px)"></div></td><td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">Tesla, Inc.</td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)" aria-label="Price (Intraday)"><fin-streamer data-test="colorChange" class="" data-symbol="TSLA" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="243.2001" active="">
<span class="e3b14781 e983cf79">243.00</span></fin-streamer></td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)" aria-label="Change"><fin-streamer data-test="colorChange" class="Fw(600)" data-symbol="TSLA" data-field="regularMarketChange" data-trend="txt" data-pricehint="2" value="5.7901" active=""><span class="e3b14781 f4be3290 e983cf79">+5.59</span></fin-streamer></td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)" aria-label="% Change"><fin-streamer data-test="colorChange" class="Fw(600)" data-symbol="TSLA" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="2" value="2.4388611" active="">
<span class="e3b14781 f4be3290 dde7f18a">+2.35%</span></fin-streamer></td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Fz(s)" aria-label="Volume"><fin-streamer data-test="colorChange" class="" data-symbol="TSLA" data-field="regularMarketVolume" data-trend="none" data-pricehint="2" value="122481541" active=""><span class="e3b14781 f5a023e1">123.919M</span></fin-streamer></td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Fz(s)" aria-label="Avg Vol (3 month)">120.549M</td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Pend(10px) W(120px) Fz(s)" aria-label="Market Cap"><fin-streamer data-test="colorChange" class="" data-symbol="TSLA" data-field="marketCap" data-trend="none" data-pricehint="2" value="773113643008" active="">773.114B</fin-streamer></td>
<td colspan="" class="Va(m) Ta(end) Pstart(20px) Fz(s)" aria-label="PE Ratio (TTM)">78.20</td><td colspan="" class="Va(m) Ta(end) Pstart(20px) Pend(6px) Fz(s)" 
aria-label="52 Week Range"><canvas style="width: 140px; height: 23px;" width="280" height="46"></canvas></td></tr>
"""
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
        if link:
            symbol = link.text
            link_href = link['href']
            link_href = "https://finance.yahoo.com" + link['href']
            most_actives_tickers[symbol] = {'url': link_href, 'price': float(price)}

    return most_actives_tickers

# NEXT BUTTON
"""
<button aria-disabled="false" class="Va(m) H(20px) Bd(0) M(0) P(0) Fz(s) Pstart(10px) O(n):f Fw(500) C($linkColor)" fdprocessedid="xjuadp">
<span class="Va(m)"><span>Next</span></span>
<svg class="Va(m)! Fill($linkColor) Stk($linkColor) Cur(p)" width="18" height="18" viewBox="0 0 48 48" data-icon="caret-right" style="stroke-width: 0; vertical-align: bottom;">
<path d="M33.447 24.102L20.72 11.375c-.78-.78-2.048-.78-2.828 0-.78.78-.78 2.047 0 2.828l9.9 9.9-9.9 9.9c-.78.78-.78 2.047 0 2.827.78.78 2.047.78 2.828 0l12.727-12.728z"></path></svg></button>
"""

# Price now
"""
<fin-streamer data-test="colorChange" 
class="" data-symbol="TSLA" data-field="regularMarketPrice" data-trend="none" 
data-pricehint="2" value="243.9544" active=""><span class="e3b14781 dde7f18a">243.33</span></fin-streamer>
"""

most_actives = "https://finance.yahoo.com/most-active"

dict_pair = scrape_listed_stocks_data(most_actives)
for symbol, url in dict_pair.items():
    print(symbol, url)

# stock_symbols = ['']
# stock_symbol = str(input())
# # url_history = ""
# url_profile = f"https://finance.yahoo.com/quote/{}?p={}"
# # url_financial =
# response = requests.get(url_profile)
# soup = BeautifulSoup(response.text, 'lxml')
# # print(soup)
#
# """
# <fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="TSLA" data-test="qsp-price"
# data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="237.41" active="">237.41</fin-streamer>
#
# <div class="D(ib) Mend(20px)"><fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="TSLA" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="237.41" active="">237.41</fin-streamer><fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="TSLA" data-test="qsp-price-change" data-field="regularMarketChange" data-trend="txt" data-pricehint="2" value="13.699997" active=""><span class="C($positiveColor)">+13.70</span></fin-streamer> <fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="TSLA" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="2" data-template="({fmt})" value="0.06123998" active=""><span class="C($positiveColor)">(+6.12%)</span></fin-streamer><fin-streamer class="D(n)" data-symbol="TSLA" changeev="regularTimeChange" data-field="regularMarketTime" data-trend="none" value="" active="true"></fin-streamer><fin-streamer class="D(n)" data-symbol="TSLA" changeev="marketState" data-field="marketState" data-trend="none" value="" active="true"></fin-streamer><div id="quote-market-notice" class="C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm Whs(n)"><span>
# At close: November 14 04:00PM EST</span></div></div>
# """
#
# price = soup.find_all('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})[0].text
# print(price)
#
# # import yfinance as yf
# # ticker_name = "TSLA"
# # ticker = yf.Ticker(ticker_name)
# # historical_data = ticker.history(period='1d')['Close']
# #
# # data_as_json = historical_data.reset_index().to_json(orient='records', date_format='iso')
# #
# # print(data_as_json)
