from src.prepare_data_in_record_format import PrepareDataInRecordFormat
from src.google_sheets_exporter import GoogleSheetsExporter
from src.excel_exporter import ExcelExporter


class ScrapeInfoOperator:
    """
    This class serves as an operator to handle the entire process of scraping financial information,
    preparing it in a specific format, and exporting it to both an Excel file and Google Sheets.

    The class utilizes other components to fetch data, process it, and then export it in the desired formats.
    Class has interaction with three other classes - PrepareDataInRecordFormat, from which takes data;
    GoogleSheetsExporter - which exports data in Google Sheets;
    ExcelExporter - which exports data in Excel table
    """
    def __init__(self):
        self.__data_holder = PrepareDataInRecordFormat()
        self.__data = self.__data_holder.final_data
        self.__sheet_name = 'Real Time Stock'
        self.__google_exporter = GoogleSheetsExporter(self.__data, self.__sheet_name)
        self.__excel_file_name = 'src/tickers_stock_data.xlsx'
        self.__excel_exporter = ExcelExporter(self.__data, self.__excel_file_name)

    def export_to_excel(self):
        """
        Exports the formatted data to an Excel file.
        :return:
        """
        self.__excel_exporter.export_data()

    def export_to_google_sheets(self):
        """
        Exports the formatted data to Google Sheets.
        :return:
        """
        self.__google_exporter.export_data()

    def main(self):
        """
        The main method to orchestrate the scraping, processing, and exporting of data.

        It first exports data to an Excel file and then prompts the user to choose if
        they want to export the data to Google Sheets as well. Handles exceptions during the process.
        :return:
        """
        try:
            self.export_to_excel()
            user_choice = input("Do you want to export in Google Sheet, too? (y/n) ")
            if user_choice.lower() != 'y':
                print("Thank you for using Reni's finance info app!")
            else:
                self.export_to_google_sheets()
        except Exception as e:
            print(f"Exception was occur {e}")


