class DataFilter:
    """
    Class witch filters collected data by finding repeating date-hours-minutes period between different tickers
    """
    def __init__(self, collected_data):
        self.collected_data = collected_data

    def filter_based_on_longest_daily_info(self):
        """
        Filter data based on longest historical info, that is already collected in ticker info.
        This is guarantees that we receive as most combination when is time for calculating arbitrage
        :return:
        """
        longest_daily_info_ticker = max(self.collected_data,
                                        key=lambda ticker: len(self.collected_data[ticker]['daily_info']))
        longest_daily_info = self.collected_data[longest_daily_info_ticker]['daily_info']
        for ticker, info in self.collected_data.items():
            if ticker != longest_daily_info_ticker:
                filtered_daily_info = {time: value for time, value in info['daily_info'].items() if
                                       time in longest_daily_info}
                self.collected_data[ticker]['daily_info'] = filtered_daily_info
