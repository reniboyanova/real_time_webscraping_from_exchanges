class Defines:
    def __init__(self):
        self.__api_key_file = 'api_token.txt'
        self.gs_ls_most_act = {'gainers': 'top_gainers', 'losers': 'top_losers', 'most-actives': 'most_actively_traded'}
        self.__gs_ls_most_act_url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey='
        self.__best_matches_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='

    @property
    def api_key_file(self):
        return self.__api_key_file


    @property
    def gs_ls_most_act_url(self):
        return self.__gs_ls_most_act_url

    @gs_ls_most_act_url.setter
    def gs_ls_most_act_url(self, url):
        self.__gs_ls_most_act_url = url
    @property
    def best_matches_url(self):
        return self.__best_matches_url

    @best_matches_url.setter
    def best_matches_url(self, url):
        self.__best_matches_url = url

    @property
    def time_daily_info_url(self):
        return self.__time_daily_info_url

    @time_daily_info_url.setter
    def time_daily_info_url(self, url):
        self.__time_daily_info_url = url

