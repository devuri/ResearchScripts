# -*- coding: utf-8 -*-

"""
This program visits the UN General Assembly website (after a search) and downloads detailed voting records and
resolution details for a certain session.

IMPORTANT:
URL variable will need to be updated when search criteria (and thus search results) are changed
In the URL variable string, replace "npp=50" with "npp=1000". If there are 1000 or fewer results, you will then get them all in one page.
If the Firefox driver loads the search results page but won't complete loading (but all the content is there), manually press the
"X" button to get the page to stop loading. Program will then continue as usual.
"""


#import statements
from selenium import webdriver
from time import sleep
from random import uniform


#isResolutionNumber returns a boolean indicating whether str is a UN Resolution Number
def isResolutionNumber(str):
    if len(str) < 20 and "RES" in str and "/" in str and ("0" in str or "1" in str or "2" in str or "3" in str or "4" in str or "5" in str or "6" in str or "7" in str or "8" in str or "9" in str):
        return True
    else:
        return False


#Directory of Folder to Contain Individual Resolutions Details
LOCAL_RESOLUTIONS_DETAILS_DIRECTORY = '' #Fill in
#Directory of Folder to Contain Individual Voting Details
LOCAL_VOTING_DETAILS_DIRECTORY = '' #Fill in
#Search Results Page
URL = 'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=14TL795717R58.370&menu=search&aspect=power&npp=1000&ipp=20&spp=20&profile=voting&ri=&index=.VM&term=A%2FRES%2F71&matchoptbox=0%7C0&oper=AND&x=19&y=11&aspect=power&index=.VW&term=&matchoptbox=0%7C0&oper=AND&index=.AD&term=&matchoptbox=0%7C0&oper=AND&index=BIB&term=&matchoptbox=0%7C0&limitbox_1=VV01+%3D+vv_rec&ultype=PD01&uloper=%3E&ullimit=2014&ultype=&uloper=%3D&ullimit=&sort='
#'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=147658G19E50U.16297&menu=search&aspect=power&npp=100&ipp=20&spp=20&profile=voting&ri=&index=.VM&term=A%2FRES%2F68&matchoptbox=0%7C0&oper=AND&x=11&y=7&aspect=power&index=.VW&term=&matchoptbox=0%7C0&oper=AND&index=.AD&term=&matchoptbox=0%7C0&oper=AND&index=BIB&term=&matchoptbox=0%7C0&limitbox_1=VV01+%3D+vv_rec&ultype=PD01&uloper=%3E&ullimit=2011&ultype=&uloper=%3D&ullimit=&sort='
#'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=1A689702368NC.429&menu=search&aspect=power&npp=100&ipp=20&spp=20&profile=voting&ri=&index=.VM&term=A%2FRES%2F69&matchoptbox=0%7C0&oper=AND&x=9&y=8&aspect=power&index=.VW&term=&matchoptbox=0%7C0&oper=AND&index=.AD&term=&matchoptbox=0%7C0&oper=AND&index=BIB&term=&matchoptbox=0%7C0&limitbox_1=VV01+%3D+vv_rec&ultype=PD01&uloper=%3E&ullimit=2010&ultype=&uloper=%3D&ullimit=&sort='
#'http://unbisnet.un.org:8080/ipac20/ipac.jsp?session=14S835V763I24.19421&menu=search&aspect=power&npp=1000&ipp=20&spp=20&profile=voting&ri=&index=.VM&term=A%2FRES%2F70&matchoptbox=0%7C0&oper=AND&x=19&y=6&aspect=power&index=.VW&term=&matchoptbox=0%7C0&oper=AND&index=.AD&term=&matchoptbox=0%7C0&oper=AND&index=BIB&term=&matchoptbox=0%7C0&limitbox_1=VV01+%3D+vv_rec&ultype=&uloper=%3D&ullimit=&ultype=&uloper=%3D&ullimit=&sort='


#Go directly to search results page
driver = webdriver.Firefox()
driver.get(URL)
sleep(uniform(5,6)) #give webpage time to load


#count the number of Resolutions
count = 0

#make a list of links to individual resolutions
for i in range(len(driver.find_elements_by_class_name('smallAnchor'))):
    #linkText is the textual content of each individual link
    linkText = driver.find_elements_by_class_name('smallAnchor')[i].text.strip('\n')
    if isResolutionNumber(linkText):
        linkText = linkText.replace('/','\\') #needed because the file names are resolution numbers (text files can't have '/' in their names)

        count += 1
        driver.find_elements_by_class_name('smallAnchor')[i].click() #we need to explicitly find the next element each time because the page is renewed every time we go back
        sleep(uniform(2,3))

        #write a resolutions details file (excluding voting details) in which the resolution number is the filename
        r = open(LOCAL_RESOLUTIONS_DETAILS_DIRECTORY + linkText + '.txt', 'w')
        #write a voting details file in which the resolution number is the filename
        v = open(LOCAL_VOTING_DETAILS_DIRECTORY + linkText + '.txt', 'w')

        #narrow down to table, then find the black print containing info
        elements = driver.find_element_by_name('full').find_elements_by_class_name('normalBlackFont1')

        #elementNum keeps track of the element number
        elementNum = 0
        for element in elements:
            elementNum += 1
            info = element.get_attribute('innerHTML').replace('\t','')
            #if info is a category
            if "&nbsp" in info:
                detailedVoting = False
                #set flag to True if category is Detailed Voting (this way we know later to write to the detailed voting file)
                if "Detailed Voting" in info:
                    detailedVoting = True
                else:
                    if elementNum != 1: #don't need a newline for the very first line
                        r.write('\n')
                    r.write(info.replace('\n','').replace('&nbsp','').strip(';'))
                    r.write('\t')
                #Agenda Information info is made of links, so it needs to be extracted separately
                if "Agenda Information" in info:
                    agendaInfo = driver.find_element_by_partial_link_text('Agenda Information').find_element_by_xpath('..').find_element_by_xpath('..').find_elements_by_class_name('smallAnchor')
                    for phrase in agendaInfo:
                        r.write(phrase.text.replace('\t','').strip('\n'))
                        r.write(';')
            else:
                #if statement to decide which file to write to
                if detailedVoting:
                    v.write(info.replace('\n',';'))
                    v.write('\n')
                else:
                    r.write(info.replace('\n',';'))
                    r.write(';')

        v.close()
        r.close()

        #navigate back one page to search results page
        driver.back()
        sleep(uniform(2,3))

print count, "Resolutions" #check that this number is correct!