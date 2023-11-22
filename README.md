# ACSM 1.0 - Arbitrage Calculation for Stock Markets


## Description:

ACSM 1.0 is a sophisticated application specifically designed to uncover arbitrage opportunities across various stock markets. It meticulously processes financial data and outputs the results in an Excel file. Additionally, there's an option to export this data to Google Sheets for enhanced accessibility and analysis.
This version sources company information in the format of company_name: [ticker_symbol, ticker_symbol2, ... etc.] from an integrated 'library', represented as a JSON file. 

It's noteworthy that this static representation serves as a snapshot and does not fully capture the dynamic and real-time essence of the app, which actively scrapes and processes live data.

To ensure the accuracy and timeliness of financial information, ACSM 1.0 leverages the Yahoo Finance API for all arbitrage calculations.


## Installation
To set up ACSM 1.0, you'll need to install the necessary libraries. 
You can do this by running the following command in your terminal: 

'pip install -r requirements.txt'.

This command will automatically install all the libraries listed in the requirements.txt file.

## Usage Instructions
To start the application, run the following command: 'python main.py'

## Configuration
For those opting to use Google Sheets for data export, additional configuration is required:

1. Obtain your Google API credentials by visiting Google Cloud Console.
2. Ensure that both the Google Sheets API and Google Drive API are enabled for your project.
3. Place your credentials JSON file in the project directory and reference it appropriately within the application.

These steps are crucial to enable seamless integration with Google Sheets and ensure the functionality of the export feature