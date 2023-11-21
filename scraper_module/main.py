from scraper_module.scrape_info_operator import ScrapeInfoOperator
"""
This program makes an arbitrage calculation 
Here we start program, and at the end of it in directory will have a excel file with information
"""

if __name__ == "__main__":
    scrape = ScrapeInfoOperator()
    scrape.main()
