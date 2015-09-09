# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml.html import fromstring
from scrapy.http import Request
from lxml.html import fromstring

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import re
import yaml
import os

class Tax1spiderSpider(scrapy.Spider):
    name = "tax1spider"
    allowed_domains = ["tax1.co.monmouth.nj.us"]
    start_urls = (
        'http://www.google.com',
    )

    def get_counties_and_towns(self, file='counties-and-towns-list.yml'):
        counties = yaml.safe_load(open(file))
        return counties

    def parse(self, response):
        file_counties = self.get_counties_and_towns()
        try:
            options = webdriver.ChromeOptions()
            # prefs = {"download.default_directory" : "c://files", "directory_upgrade": True}
            options.add_experimental_option('prefs', {'download.default_directory':'C:\\files'})
            # options.add_experimental_option("prefs",prefs)
            options.add_argument("--start-maximized")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-java")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-images")
            driver = webdriver.Chrome('c://chromedriver.exe',chrome_options = options)
            driver.get('http://tax1.co.monmouth.nj.us/cgi-bin/prc6.cgi?&ms_user=monm&passwd=data&district=1401&srch_type=0&adv=0&out_type=3')
            time.sleep(3)

            html = driver.page_source
            hxs = fromstring(html)
            counties = hxs.xpath('//select[@name="select_cc"]/option/text()')
            counties_value = hxs.xpath('//select[@name="select_cc"]/option/@value')
            counties_and_value = dict(zip(counties,counties_value))

            # time.sleep(1)
            # html = driver.page_source
            # hxs = fromstring(html)
            # towns = hxs.xpath('//select[@name="district"]/option/text()')

            print counties
            # print towns

            for county in file_counties.keys():
                county = county.split()[0].upper()
                """
                checking if file county key exist in site county drop down
                """
                if county in counties:
                    county_id = counties_and_value[county]
                    driver.get('http://tax1.co.monmouth.nj.us/cgi-bin/prc6.cgi?&ms_user=monm&passwd=data&district={}&srch_type=0&adv=0&out_type=3'.format(county_id))
                    time.sleep(2)
                    """
                    Getting all towns of selected County
                    """
                    html = driver.page_source
                    hxs = fromstring(html)
                    districts = hxs.xpath('//select[@name="district"]/option/text()')

                    """
                    Retrieving each county districts list
                    """
                    for file_districts in file_counties.values():
                        """
                        Iterating each list of county districts which is list
                        """
                        for file_district in file_districts:
                            """
                            File district matches district from site
                            """
                            if file_district.upper() in districts:
                                """
                                Selecting district from dropdown
                                """
                                driver.find_element_by_xpath("//select[@name='district']/option[text()='{}']".format(file_district.upper())).click()
                                print "finally shit happens"


                                with open('check.html','w') as mf:
                                    mf.write(driver.page_source)
                                """
                                Actual downloading goes here
                                """
                                time.sleep(3)
                                driver.find_element_by_xpath('//input[@type="Submit"]').click()
                                time.sleep(2)
                                file_name = driver.find_element_by_xpath('//a[@target="output"]').get_attribute("href")
                                if file_name:
                                    file_name = file_name.rsplit('/',1)[1]
                                    if file_name in os.listdir('c://files'):
                                        time.sleep(3)
                                        driver.back()
                                        continue

                                driver.find_element_by_xpath('//a[@target="output"]').click()
                                time.sleep(10)
                                driver.back()
                                time.sleep(3)

                    print county
                    print "found"


        except Exception as e:
            print e
