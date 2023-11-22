from src.helprers import  convert_to_utc_time

class TickerDataProcessor:
    @staticmethod
    def format_historical_data(historical_data, timezone):
        formatted_data = {}
        for index, row in historical_data.iterrows():
            utc_time = convert_to_utc_time(str(index.time()), str(index.date()), timezone)
            formatted_data[utc_time] = row['Close']
        return formatted_data
