"""
This program extracts the content html from an online court resolution when given the url. It then writes
files for individual resolution report tables.
"""

#import statements
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

#Location of URL File
URL_FILE = '' #Fill in
#Directory of Folder to Contain Tables as Text Files
LOCAL_REPORT_DIRECTORY = '' #Fill in
#Location of file to contain all urls that are empty
EMPTY_URLS = '' #Fill in
#Location of file to contain all urls that have no table
NO_TABLE_URLS = '' #Fill in

#e is the file that contains the empty URLs
e = open(EMPTY_URLS, 'w')

#n is the file that contains the no tables URLs
n = open(NO_TABLE_URLS, 'w')

#u is the file that contains all the urls
u = open(URL_FILE, 'r')
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

    #if url leads to a blank page or did not load properly
    if not viewReportLXML.find("p"):
        e.write(url)
        e.write('\n')

    elif viewReportLXML.find("table"):
        f = open((LOCAL_REPORT_DIRECTORY + url[32:] + '.txt'), 'w')
        for item in viewReportLXML.find_all('table'):
            for thing in item.find_all('tr'):
                for box in thing.find_all('td'):
                    for i in box.find_all('p'):
                        f.write(i.get_text().encode('utf-8').replace('\n',' ').replace('\t',' ').strip(' '))
                        f.write(';')
                    f.write('\t')
                f.write('\n')
        f.close()
    else: #no table found
        n.write(url)
        n.write('\n')

n.close()
e.close()
u.close()