from prepare_data_in_record_format import PrepareDataInRecordFormat
from google_sheets_importer import GoogleSheetsImporter


class ScrapeInfoOperator:
    def __init__(self):
        self.__data_holder = PrepareDataInRecordFormat()
        self.__data = self.__data_holder.final_data
        self.__sheet_name = 'Real Time Stock'
        self.__google_importer = GoogleSheetsImporter(self.__data, self.__sheet_name)

    def main(self):
        self.__google_importer.import_to_google_sheets()



if __name__ == "__main__":
    scrape = ScrapeInfoOperator()
    scrape.main()