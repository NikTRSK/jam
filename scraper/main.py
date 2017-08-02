from db_connector import db_connector
from glassdoorScraper import GlassdoorScraper

def main():
    db = db_connector()
    scraper = GlassdoorScraper(db)
    scraper.searchJobs()

main()