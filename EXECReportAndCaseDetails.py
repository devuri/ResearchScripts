"""
This program visits a list of court report urls, clicks to get case details, then extracts the court reports and
the case details to write files in a formatted order.
"""

#import statements
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import uniform

#Location of URL File
URL_FILE = '' #Fill in with location of text file with a list of URLs
#Directory of Folder to Contain Reports
LOCAL_REPORT_DIRECTORY = '' #Fill in with location of folder to contain judgment reports
#Location of file to contain all urls that lead to a pick language interface or empty container
EXCEPTION_URLS = '' #Fill in with location of text file to contain empty-page urls
#Directory of Folder to Contain Individual Case Details
LOCAL_CASE_DIRECTORY = '' #Fill in with location of folder to contain case details

#e is the file that contains the exception URLs
e = open(EXCEPTION_URLS, 'w')

#u is the file that contains all the urls
u = open(URL_FILE, 'r')
urlList = u.readlines()
u.close()

#open a Firefox browser
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
    sleep(uniform(6,7)) #give webpage time to load
    information = driver.find_element_by_class_name('content')
    viewReportLXML = BeautifulSoup(information.get_attribute('innerHTML'), 'lxml')
    #if url actually leads to a court report
    if viewReportLXML.find("p"):
        f = open((LOCAL_REPORT_DIRECTORY + url[32:].strip('\n') + '.txt'), 'w')
        for item in viewReportLXML.find_all("p"):
            f.write(item.get_text().encode('utf-8'))
            f.write('\n')
        f.close()
    #if url leads to a pick language interface or empty container
    else:
        e.write(url.strip('\n'))
        e.write('\n')

    #Case Details
    driver.find_element_by_id('notice').click() #click the notice button
    sleep(uniform(6,7)) #give webpage time to load
    page_source = BeautifulSoup(driver.page_source, 'lxml') #parse page HTML with BeautifulSoup

    #write Case Details to file c in formatted order
    #Each line of local file has subject  + tab + subject info for court case
    #Example: 'Originating Body' + '\t'+ ' Court (Chamber) '
    c = open(LOCAL_CASE_DIRECTORY + url[32:].strip('\n') + '.txt', 'w')
    for item in page_source.select('div.noticefield'):
        for title in item.select('div.span2.noticefieldheading'):
            for thing in title.get_text().encode('utf-8').replace('\n','').replace('\t',''), '\t',:
                c.write(thing)
        for answer in item.select('div.offset2.noticefieldvalue'):
            for thing in answer.get_text().encode('utf-8').replace('\n',';').replace('\t',''):
                c.write(thing)
            c.write('\n')
    c.close()

e.close()