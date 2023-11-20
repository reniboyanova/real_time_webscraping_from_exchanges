from helprers import get_api_key, prompt_user_to_paste_ticker
from different_approacher import defines_

import requests
from requests import RequestException

de = defines_.Defines()


class NewTickersCollector:
    def __init__(self):
        self.__api_key_file = 'alpha_api.txt'
        self.__api_key = get_api_key(self.__api_key_file)
        self.__new_ticker = {}

    def __find_best_matches(self, company_or_ticker_search):
        url = f'{de.best_matches_url}{self.__api_key}'

        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": company_or_ticker_search,
            "apikey": self.__api_key,
            "datatype": "json"
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()

            for match in data['bestMatches']:
                company_name = match.get('2. name', '').lower()
                self.__new_ticker[company_name] = []
                if company_name in self.__new_ticker:
                    self.__new_ticker[company_name].append(match.get('1. symbol', ''))

        except RequestException as e:
            print(f"Error war occurred: {e}")

    def __only_more_than_one_match(self):
        if self.__new_ticker:
            max_length = max(len(tickers) for tickers in self.__new_ticker.values())

            self.__new_ticker = {company: tickers for company, tickers in self.__new_ticker.items() if
                                 len(tickers) == max_length}
            return
        raise ValueError("Missing information, self.__new_ticker is empty!")

    @property
    def new_ticker(self):
        return self.__new_ticker

    def process_new_ticker(self):
        self.__find_best_matches(prompt_user_to_paste_ticker())


if __name__ == "__main__":
    new_t = NewTickersCollector()
    new_t.process_new_ticker()
    print(new_t.new_ticker)