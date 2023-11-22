from src.scrape_info_operator import ScrapeInfoOperator
import logging

logging.basicConfig(level=logging.INFO, filename="loging_info.log", filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        scrape = ScrapeInfoOperator()
        scrape.main()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")

