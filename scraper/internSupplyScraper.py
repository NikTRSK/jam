from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import pymongo

class InternSupplyScraper:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['jobs']
        self.jobs = self.db.jobs
        # import pprint
        # pprint.pprint(self.jobs.insert_one({ "company": "Google" }))
        # pprint.pprint(self.jobs.find_one( {"company": "Google"} ))

    def getCompanyList(self):
        url = "http://www.intern.supply/"
        webpage = urlopen(url)
        html = BeautifulSoup(webpage.read(), "lxml")
        allCompanies = html.find_all('article')
        # print(allCompanies)
        companyList = self.parseAllTags(allCompanies[1:])

    def parseAllTags(self, companies):
        for company in companies:
            entry = {}
            entry['company'] = company.h3.text
            locations = (company.find_all('i'))
            if len(locations) > 1:
                entry['location'] = locations[1]['title']
            else:
                entry['location'] = None
            entry['application_open'] = None
            entry['job_link'] = None
            entry['cover_letter'] = None
            entry['resume'] = None
            entry['applied'] = None
            entry['salry_estimate'] = None
            if (self.jobs.find_one({ "company": entry['company'] })) is None:
                self.jobs.insert_one(entry)

scraper = InternSupplyScraper()
scraper.getCompanyList()