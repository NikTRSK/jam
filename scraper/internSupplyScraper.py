from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re

class InternSupplyScraper:

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
            print(entry)
        # print(tags[0].h3.text)
        # iTags = tags[0].find_all('i')
        # print(iTags[1]['title'])


scraper = InternSupplyScraper()
scraper.getCompanyList()