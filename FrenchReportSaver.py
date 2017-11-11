"""
This program visits URLs that fall under "EmptyReportExceptions", meaning the full judgments lead to a pick language
interface or to a blank document. The program then finds the URL to the French copy of the full judgment through the HTML
code, visits the French URL, and extracts the content html from an online French court report. It then writes files for
individual court reports and a list of the original URLs that didn't have a link to a French page.
"""

#import statements
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from random import uniform

#Location of URL File
URL_FILE = '' #Fill in with location of text file with list of URLs
#Directory of Folder to Contain French Reports
LOCAL_REPORT_DIRECTORY = '' #Fill in with location of folder that contains reports
#Location of file to contain all urls that lead to a non-French pick language interface or empty container
EXCEPTION_URLS = '' #Fill in with location of text file with a list of exception URLs (blank page)

BASE_URL = 'http://hudoc.echr.coe.int/eng?i='

#e is the file that contains the new exception URLs
e = open(EXCEPTION_URLS, 'w')


#u is the file that contains all the urls
u = open(URL_FILE, 'r')
urlList = u.readlines()
u.close()

driver = webdriver.Firefox()

count = 0

for url in urlList:
    count += 1
    if count % 100 == 0:
        driver.quit()
        sleep(5)
        driver = webdriver.Firefox()
        sleep(5)

    driver.get(url)
    sleep(uniform(7,8)) #give webpage time to load

    #FAILED Attempts
    #clicks on blank space to right of link, though even if we did click it we would open a new window
    #driver.find_element_by_class_name('languageEntry').click()
    #driver.find_element_by_css_selector('div.languageEntry').click()
    #locates the link but it isn't clickable
    #driver.find_element_by_link_text('French').click()

    frenchURL = ""
    foundFrenchURL = False

    #we don't want the program to crash if the language interface is blank, so we have a try-except statement
    try:
        idLoc = driver.find_element_by_class_name('languageEntry')
        frenchID = BeautifulSoup(idLoc.get_attribute('innerHTML'), 'lxml')
        if "french" in frenchID.get_text().lower(): #if link is French
            for phrase in frenchID.find('a')['href'].split(':'):
                if '001-' in phrase: #if itemid in phrase
                    frenchURL = BASE_URL + phrase.split('\"')[1] #get itemid in quotes and append to BASE_URL
                    foundFrenchURL = True
    #there is no other full judgment in existence ie. just a completely blank document with no links
    except NoSuchElementException:
        foundFrenchURL = False

    if foundFrenchURL:
        driver.get(frenchURL)
        sleep(uniform(7,8)) #give webpage time to load
        information = driver.find_element_by_class_name('content')
        viewReportLXML = BeautifulSoup(information.get_attribute('innerHTML'), 'lxml')
        #if url actually leads to a court report
        if viewReportLXML.find("p"):
            f = open((LOCAL_REPORT_DIRECTORY + url[32:].strip('\n') + '.txt'), 'w')
            f.write(frenchURL)
            f.write('\n')
            for item in viewReportLXML.find_all("p"):
                f.write(item.get_text().encode('utf-8'))
                f.write('\n')
            f.close()
    #if there is no link to a french URL, write the original URL to the exception list
    else:
        e.write(url.strip('\n'))
        e.write('\n')

e.close()