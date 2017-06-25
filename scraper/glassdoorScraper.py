from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import pymongo
from selenium import webdriver
from splinter import Browser
from selenium.webdriver.chrome.options import Options

class GlassdoorScraper:
    def __init__(self):
        self.baseURL = r"https://www.glassdoor.com/index.htm"
        self.searchTerms = ["software engineer new grad", "software developer new grad",
                            "software engineer recent grad", "software developer recent grad"]
        self.cities = ["chicago", "new york", "boston", "seattle", "philadelphia",
                       "los angeles", "santa monica", "venice, ca", "san francisco",
                       "mountain view", "palo alto", "menlo park", "san mateo", "daly city", "oakland"]

        self.browser = self.init_glasdoor()

    def init_glasdoor(self):
        chrome_options = Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--start-maximized")
        browser = Browser('chrome', options=chrome_options)
        return browser

    def searchJobs(self):
        for job in self.searchTerms:
            for city in self.cities:
                self.searchJob(job, city)
                break #remove
            break #remove

    def searchJob(self, job, city):
        # browser = self.init_glasdoor()
        browser = self.browser
        browser.visit(self.baseURL)
        searchJobBox = browser.find_by_id("KeywordSearch")
        searchLocBox = browser.find_by_id("LocationSearch")
        searchBtn = browser.find_by_id("HeroSearchButton")
        searchJobBox.fill(job)
        searchLocBox.fill(city)
        searchBtn.click()

        jobList = browser.find_by_css("jlGrid hover")
        print(jobList)

        # import pprint
        # pprint.pprint(self.jobs.insert_one({ "company": "Google" }))
        # pprint.pprint(self.jobs.find_one( {"company": "Google"} ))

    # def getCompanyList(self):
    #     url = "http://www.intern.supply/"
    #     webpage = urlopen(url)
    #     html = BeautifulSoup(webpage.read(), "lxml")
    #     allCompanies = html.find_all('article')
    #     # print(allCompanies)
    #     companyList = self.parseAllTags(allCompanies[1:])
    #
    # def parseAllTags(self, companies):
    #     for company in companies:
    #         entry = {}
    #         entry['company'] = company.h3.text
    #         locations = (company.find_all('i'))
    #         if len(locations) > 1:
    #             entry['location'] = locations[1]['title']
    #         else:
    #             entry['location'] = None
    #         entry['application_open'] = None
    #         entry['job_link'] = None
    #         entry['cover_letter'] = None
    #         entry['resume'] = None
    #         entry['applied'] = None
    #         entry['salry_estimate'] = None
    #         if (self.jobs.find_one({ "company": entry['company'] })) is None:
    #             self.jobs.insert_one(entry)

scraper = GlassdoorScraper()
scraper.searchJobs()