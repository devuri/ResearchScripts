"""
This program visits a list of court report urls, clicks to get case details, then extracts the case details
to write files in a formatted order.
"""

#import statements
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from random import uniform

#Location of URL File
URL_FILE = '' #Fill in (text file)
#Directory of Folder to Contain Individual Case Details
LOCAL_REPORT_DIRECTORY = '' #Fill in (folder)

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
    driver.find_element_by_id('notice').click() #click the notice button
    sleep(uniform(6,7)) #give webpage time to load
    page_source = BeautifulSoup(driver.page_source, 'lxml') #parse page HTML with BeautifulSoup

    #write Case Details to file c in formatted order
    #Each line of local file has subject  + tab + subject info for court case
    #Example: 'Originating Body' + '\t'+ ' Court (Chamber) '
    c = open(LOCAL_REPORT_DIRECTORY + url[32:].strip('\n') + '.txt', 'w')
    for item in page_source.select('div.noticefield'):
        for title in item.select('div.span2.noticefieldheading'):
            for thing in title.get_text().encode('utf-8').replace('\n','').replace('\t',''), '\t',:
                c.write(thing)
        for answer in item.select('div.offset2.noticefieldvalue'):
            for thing in answer.get_text().encode('utf-8').replace('\n',';').replace('\t',''):
                c.write(thing)
            c.write('\n')
    c.close()