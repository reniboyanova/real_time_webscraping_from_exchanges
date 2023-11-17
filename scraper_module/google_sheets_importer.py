import json
import pandas as pd
import pygsheets

def import_to_google_sheets():
    """
    Imports data from a JSON file into a Google Sheets spreadsheet using the pygsheets library.
    """

    google_client = pygsheets.authorize(service_file="credentials.json")

    spreadsheet = google_client.open("Real Time Stock")

    work_sheet = spreadsheet[0] if input("Do you want to open new sheet? (y/n) ").lower() == 'n' \
        else spreadsheet.add_worksheet(input("Input the name of sheet, please: "))

    # Clear the existing sheet if it's the first sheet in the spreadsheet
    if work_sheet == spreadsheet[0]:
        work_sheet.clear()

    with open("most_active_stocks.json", "r") as json_file:
        data = json.load(json_file)

    # Define the columns for the data
    result = {
        "Ticker": [],
        "Price": [],
        "URL": []
    }

    for ticker, details in data.items():
        result["Ticker"].append(ticker)
        result["Price"].append(details.get("price", ""))
        result["URL"].append(details.get("url", ""))

    work_sheet.set_dataframe(pd.DataFrame(result), 'A1')

if __name__ == "__main__":
    import_to_google_sheets()
