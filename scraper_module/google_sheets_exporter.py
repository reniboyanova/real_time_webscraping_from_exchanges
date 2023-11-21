import pygsheets

from scraper_module.data_exporter import DataExporter


class GoogleSheetsExporter(DataExporter):
    """
       GoogleSheetsExporter derive DataExporter and extends its method export_data.
        This class uses module 'pygsheets' to store data.
        To use it, you also need to have Google Sheets API credentials.
        """
    def __init__(self, data, spreadsheet_name):
        super().__init__(data)
        self.spreadsheet_name = spreadsheet_name
        self.google_client = pygsheets.authorize(service_file="credentials.json")
        self.spreadsheet = self.google_client.open(self.spreadsheet_name)

    def export_data(self):
        """
        Overrides base class method with logic for GoogleSheets exporting
        :return:
        """
        for info in self.data:
            try:
                work_sheet = self.spreadsheet.worksheet_by_title(info['Company Ticker'])
            except pygsheets.exceptions.WorksheetNotFound:
                work_sheet = self.spreadsheet.add_worksheet(title=info['Company Ticker'])

            df = DataExporter.create_dataframe(info)
            work_sheet.clear()
            work_sheet.set_dataframe(df, 'A1')
