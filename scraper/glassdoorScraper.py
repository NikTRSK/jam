from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import pymongo
from selenium import webdriver
from splinter import Browser
from selenium.webdriver.chrome.options import Options
from time import sleep
from db_connector import db_connector

class GlassdoorScraper:
    def __init__(self, db):
        self.baseURL = r"https://www.glassdoor.com/index.htm"
        self.searchTerms = ["software engineer new grad", "software developer new grad",
                            "software engineer recent grad", "software developer recent grad"]
        self.cities = ["chicago", "new york", "boston", "seattle", "philadelphia",
                       "los angeles", "santa monica", "venice, ca", "san francisco", "san diego",
                       "mountain view", "palo alto", "menlo park", "san mateo", "daly city", "oakland"]

        self.browser = self.init_glasdoor()
        self.db = db

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
        browser = self.browser
        browser.visit(self.baseURL)
        searchJobBox = browser.find_by_id("KeywordSearch")
        searchLocBox = browser.find_by_id("LocationSearch")
        searchBtn = browser.find_by_id("HeroSearchButton")
        searchJobBox.fill(job)
        searchLocBox.fill(city)
        searchBtn.click()

        navFooter = browser.find_by_id("ResultsFooter")
        nav = navFooter.find_by_tag('ul')
        nextBtn = nav.find_by_tag('li')
        while ("disabled" not in (nextBtn.last.html)):
            jobList = browser.find_by_id("MainCol")
            self.getJobData(jobList)

            navFooter = browser.find_by_id("ResultsFooter")
            nav = navFooter.find_by_tag('ul')
            nextBtn = nav.find_by_tag('li')

            nextBtn.last.click()
            closeBtn = browser.find_by_css(".mfp-close")
            try:
                closeBtn.click()
            except AttributeError:
                print ("No close button on this page")
            # Re attach the the next button
            navFooter = browser.find_by_id("ResultsFooter")
            nav = navFooter.find_by_tag('ul')
            nextBtn = nav.find_by_tag('li')

    def getJobData(self, jobList):
        for jl in jobList:
            for l in jl.find_by_tag('li'):
                data = (l.text)
                if len(data) > 1:
                    soup = BeautifulSoup(l.html, "lxml")
                    company_city = soup.find('div', {"class": "empLoc"})
                    sleep(0.1)
                    if company_city is not None:
                        company_city = company_city.text.encode("utf-8").split(b"\xe2\x80\x93")
                        if len(company_city) is 2:
                            company = company_city[0].strip(b' ')
                            city = company_city[1].strip(b' ')

                            est_salary = soup.find('span', {"class": "green"})
                            salary = ''
                            if (est_salary) is not None:
                                salary = est_salary.text.encode("utf-8")
                            # Get job posting link
                            links = l.find_by_tag('a')
                            job_link = links['href']
                            item = {
                                "company": str(company),
                                "city": [str(city)],
                                "salary": str(salary),
                                "job_link": [str(job_link)]
                            }
                            self.db.update_company_location_if_exists(item)
                            # print(str(company) + " | " + str(city) + " | " + str(salary) + " | job: " + str(job_link) + "\n")

# scraper = GlassdoorScraper()
# scraper.searchJobs()