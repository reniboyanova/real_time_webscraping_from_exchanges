import pandas as pd

from data_exporter import DataExporter


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
        with pd.ExcelWriter(self.file_name) as writer:
            for info in self.data:
                df = DataExporter.create_dataframe(info)
                df.to_excel(writer, sheet_name=info['Company Ticker'], index=False)

