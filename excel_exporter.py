import logging

import pandas as pd

from data_exporter import DataExporter

logging.basicConfig(level=logging.INFO, filename="app.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
class ExcelExporter(DataExporter):
    """
    ExcelExporter derive DataExporter and extends its method export_data.
    This class uses module pandas as pd and 'openpyxl' to store data.
    To use it, you need to install in your terminal with command - 'pip install openpyxl'
    """
    def __init__(self, data, file_name):
        super().__init__(data)
        self.file_name = file_name

    def export_data(self):
        """
        Overrides base class method with logic for Excel exporting
        :return:
        """
        try:
            with pd.ExcelWriter(self.file_name) as writer:
                for info in self.data:
                    df = DataExporter.create_dataframe(info)
                    df.to_excel(writer, sheet_name=info['Company Ticker'], index=False)

        except (ValueError, PermissionError, FileNotFoundError) as e:
            logging.error(f"Error exporting to Excel: {e}")
            print(f"Error exporting to Excel: {e}")

