"""
This program extracts the content html from an online court report when given the url. It then writes
files for individual court reports, a cumulative court report, and a list of urls that lead
to blank pages or pages that need additional clicks to reach a non-English court report.
"""

#import statements
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

#Location of URL File
URL_FILE = '' #Fill in
#Directory of Folder to Contain reports
LOCAL_REPORT_DIRECTORY = '' #Fill in
#Location of file to contain all urls that lead to a pick language interface or empty container
EXCEPTION_URLS = '' #Fill in
#Location of file to contain all reports
CUMULATIVE_REPORT = '' #Fill in

#e is the file that contains the exception URLs
e = open(EXCEPTION_URLS, 'w')

#t is the file that contains all the reports
t = open(CUMULATIVE_REPORT, 'w')

#u is the file that contains all the urls
u =  open(URL_FILE, 'r')
urlList = u.readlines()

driver = webdriver.Firefox()

count = 0

for url in urlList:
    count += 1
    if count % 200 == 0:
        driver.quit()
        sleep(5)
        driver = webdriver.Firefox()
        sleep(5)

    driver.get(url)
    sleep(8) #give webpage time to load
    information = driver.find_element_by_class_name('content')
    viewReportLXML = BeautifulSoup(information.get_attribute('innerHTML'), 'lxml')
    #if url actually leads to a court report
    if viewReportLXML.find("p"):
        t.write('------------------------------------------------------------------------------------------\n\n')
        f = open((LOCAL_REPORT_DIRECTORY + url[32:] + '.txt'), 'w')
        for item in viewReportLXML.find_all("p"):
            f.write(item.get_text().encode('utf-8'))
            f.write('\n')
            t.write(item.get_text().encode('utf-8'))
            t.write('\n')
        f.close()
        t.write('\n\n------------------------------------------------------------------------------------------')
    #if url leads to a pick language interface or empty container
    else:
        e.write(url)
        e.write('\n')
    #now onto the "Case Details"



e.close()
t.close()
u.close()