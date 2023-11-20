import json

import pandas as pd
import pygsheets


class GoogleSheetsImporter:
    def __init__(self, data, spreadsheet_name):
        self.data = data
        self.spreadsheet_name = spreadsheet_name
        self.google_client = pygsheets.authorize(service_file="credentials.json")
        self.spreadsheet = self.google_client.open(self.spreadsheet_name)

    def import_to_google_sheets(self):
        for info in self.data:
            try:
                work_sheet = self.spreadsheet.worksheet_by_title(info['Company Ticker'])
            except pygsheets.exceptions.WorksheetNotFound:
                work_sheet = self.spreadsheet.add_worksheet(title=info['Company Ticker'])

            max_length = max([len(values) if isinstance(values, list) else 1 for values in info.values()])

            df_data = {col: [] for col in info.keys()}

            for key, values in info.items():
                if isinstance(values, list):
                    df_data[key].extend(values + [None] * (max_length - len(values)))
                else:
                    df_data[key].extend([values] * max_length)


            df = pd.DataFrame.from_dict(df_data)
            work_sheet.clear()
            work_sheet.set_dataframe(df, 'A1')


if __name__ == "__main__":
    data = [{'Company Ticker': 'AMZN', 'Exchange Name': 'NMS', 'Local Company Timezone': 'America/New_York',
                  'Local Company Currency': 'USD',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00',
                                                  '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00',
                                                  '2023-11-17 19:30:00',
                                                  '2023-11-17 20:30:00'],
                  'Close Prices in Local Currency': [144.55999755859375, 144.20010375976562, 144.3000030517578,
                                                     144.7133026123047, 144.74000549316406, 144.56500244140625,
                                                     145.17999267578125],
                  'Difference in USD with AMZN.MX': ['-0.14599428660136482 USD', '0.07033003860919962 USD',
                                                     '0.14306321143442347 USD', '0.020393562885914207 USD',
                                                     '0.20468118649878875 USD', '1.0400016423189413 USD'],
                  'Difference in USD with AMZN.NE': ['-131.79262120935275 USD', '-131.4473608409121 USD',
                                                     '-131.54726013290428 USD', '-131.9239775130032 USD',
                                                     '-131.94336367866882 USD', '-131.77567734210476 USD',
                                                     '-132.34676728531733 USD']},
                 {'Company Ticker': 'AMZN.MX', 'Exchange Name': 'MEX',
                  'Local Company Timezone': 'America/Mexico_City',
                  'Local Company Currency': 'MXN',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00',
                                                  '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00',
                                                  '2023-11-17 19:30:00'],
                  'Close Prices in Local Currency': [2484.5, 2482.030029296875, 2485.0, 2490.0, 2493.6298828125,
                                                     2504.989990234375],
                  'Difference in MXN with AMZN': ['21.743115567967834 MXN', '17.97359145315022 MXN',
                                                  '16.73557922425016 MXN', '18.90097211150487 MXN',
                                                  '15.73403833366092 MXN', '1.3398952098023074 MXN'],
                  'Difference in MXN with AMZN.NE': ['-2265.564995794089 MXN', '-2263.34595919487 MXN',
                                                     '-2266.315929897995 MXN', '-2270.688618568623 MXN',
                                                     '-2274.19303432917 MXN', '-2285.678608802998 MXN']},
                 {'Company Ticker': 'AMZN.NE', 'Exchange Name': 'NEO', 'Local Company Timezone': 'America/Toronto',
                  'Local Company Currency': 'CAD',
                  'Found time in Period in UTC': ['2023-11-17 14:30:00', '2023-11-17 15:30:00',
                                                  '2023-11-17 16:30:00',
                                                  '2023-11-17 17:30:00', '2023-11-17 18:30:00',
                                                  '2023-11-17 19:30:00',
                                                  '2023-11-17 20:30:00'],
                  'Close Prices in Local Currency': [17.450000762939453, 17.43000030517578, 17.43000030517578,
                                                     17.479999542236328, 17.489999771118164, 17.479999542236328,
                                                     17.540000915527344],
                  'Difference in CAD with AMZN': ['180.12951743133286 CAD', '179.65762770803352 CAD',
                                                  '179.79416654528524 CAD', '180.3090506052769 CAD',
                                                  '180.33554693438964 CAD', '180.10635914976297 CAD',
                                                  '180.88690478985126 CAD'],
                  'Difference in CAD with AMZN.MX': ['180.57464610781682 CAD', '180.39777996213215 CAD',
                                                     '180.6344985774281 CAD', '180.98301945884361 CAD',
                                                     '181.26233549566012 CAD', '182.17778199567525 CAD']}]

    g_sheet = GoogleSheetsImporter(data, 'Real Time Stock')
    g_sheet.import_to_google_sheets()
