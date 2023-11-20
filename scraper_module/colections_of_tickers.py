class CollectionsOfTickers:
    def __init__(self):
        self.__collection_stock_tickers = {
            'tesla': ['TSLA', 'TSLA.NE', 'TL0.DE'],
            'lufax': ['LU', '6623.HK', '6V3.F', '6V3.DU', '6V3.MU', '6V3.BE'],
            'palantir': ['PLTR', 'PLTR.VI', 'PTX.DE', 'PTX.F'],
            'nu_holdings': ['NU', 'ROXO34.SA', 'NU.CL', 'NUN.MX', 'M1Z.SG', 'M1Z.MU'],
            'plug_power': ['PLUG', 'PLUN.F', 'PLUN.DE', 'PLUG.MX', 'PLUN.SG', '0R1J.IL'],
            'amazon': ['AMZN', 'AMZN.MX', 'AMZ.DE', 'AMZN.NE', 'AMZO34.SA', 'AMZN.BA'],
            'marathon_digital': ['MARA', 'MARA.MX', 'M44.MU', 'US5657881067.SG', 'M44.F'],
            'alibaba': ['BABA', '9988.HK', 'AHLA.DE', 'AHLA.VI', 'BABAF', 'BABAN.MX'],
            'cisco_systems': ['CSCO', 'CSCO.MX', 'CSCO.NE', 'CSCO.BA', 'CIS.DE', 'CIS.BE'],
            'macy_s': ['M', 'MACY.VI', 'M.MX', 'FDO.DE', 'FDO.DU']
        }

    @property
    def collection_stock_tickers(self):
        return self.__collection_stock_tickers

    @collection_stock_tickers.setter
    def collection_stock_tickers(self, new_ticker):
        try:
            if isinstance(new_ticker, dict):
                for key, values in new_ticker.items():
                    if not isinstance(values, list):
                        raise ValueError("Ticker values for each key should be a list.")

                    if key not in self.__collection_stock_tickers:
                        self.__collection_stock_tickers[key] = values
                    else:
                        for value in values:
                            if value not in self.__collection_stock_tickers[key]:
                                self.__collection_stock_tickers[key].append(value)
            else:
                raise TypeError("New ticker must be a dictionary.")
        except Exception as e:
            print(e)
