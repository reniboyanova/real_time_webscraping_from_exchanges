from abc import ABC, abstractmethod

import pandas as pd


class DataExporter(ABC):
    """
    An abstract class with logic for exports providing data in initialization
    """
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def export_data(self):
        """
        Abstract method witch every derived class needs to implement.
        :return:
        """
        pass

    @staticmethod
    def create_dataframe(info):
        """
        Creating dataframe based on information (dictionary)
        Makes cols with every dict key's name. And adds rows by using max length of data (values)
        :param info: dictionary
        :return:
        """
        if not isinstance(info, dict):
            raise TypeError("Info needs to be a dictionary instance!")

        max_length = max([len(values) if isinstance(values, list) else 1 for values in info.values()])
        df_data = {col: [] for col in info.keys()}

        for key, values in info.items():
            if isinstance(values, list):
                df_data[key].extend(values + [''] * (max_length - len(values)))
            else:
                df_data[key].extend([values] * max_length)

        return pd.DataFrame.from_dict(df_data)