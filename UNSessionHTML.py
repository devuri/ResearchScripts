"""
This program parses the HTML UN Session reports for footnotes.
"""

#CONSTANTS - CHANGE THESE FOR DIFFERENT SESSIONS
UN_SESSION_NUMBER = 57
footnoteExpression = "TimesNewRoman; font-size:7px"
#"TimesNewRomanPSMT; font-size:7px" #Session 70,65
#"Times-Roman; font-size:9px" #Session 69,68,67
#"TimesNewRoman; font-size:7px" #Session 66,64,63,62,61,60,59,58,57



#import statements
from bs4 import BeautifulSoup
import re
import xlwt

#Location of HTML File
HTML_FILE = "/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextHTML/%d.html" %UN_SESSION_NUMBER

e = open(HTML_FILE, 'r')
soup = BeautifulSoup(e, 'lxml') #parse page HTML with BeautifulSoup
e.close()

workbook = xlwt.Workbook()
sectionNum = 0
row = 1 #row is the row of the Excel spreadsheet that will be written next (starting at zero)

footnoteList = soup.find_all(style=re.compile(footnoteExpression))
for footnote in footnoteList:
    if footnote.get_text().strip(' ') == "1":
        #make new sheet for footnotes of new section
        sectionNum += 1
        sheet = workbook.add_sheet("Section %d" %sectionNum)
        sheet.write(0,0,"Footnote #")
        sheet.write(0,1,"Footnote Text")
        row = 1
    sheet.write(row,0,footnote.get_text())
    str = ""
    for sibling in footnote.find_next_siblings():
        if sibling in footnoteList:
            break
        str = str + sibling.get_text()
    if len(str) <= 32767:
        sheet.write(row,1,str)
    else: #text is too big to fit in one cell
        sheet.write(row,1,"OVERFLOW")
        print "OVERFLOW: ", str
    row += 1
workbook.save("/Users/dongpengxia/Downloads/Footnotes%d.xls" %UN_SESSION_NUMBER)












#for footnote in soup.find_all(style="font-family: WGJKJW+TimesNewRomanPSMT; font-size:7px"): #SECTION 1 FOOTNOTES
#    print footnote
#    print footnote.get_text()

"""
footnoteList = soup.find_all(style=re.compile("font-size:7px"))
for footnote in footnoteList:
    print footnote.get_text()
    for sibling in footnote.find_next_siblings():
        if sibling in footnoteList:
            break
        print sibling.get_text(),
    print ""
"""

#SECTION 2 FOOTNOTES
"""
footnoteList = soup.find_all(style="font-family: THZHAN+TimesNewRomanPSMT; font-size:7px")
for footnote in footnoteList:
    print footnote.get_text()
    for sibling in footnote.find_next_siblings():
        if sibling in footnoteList:
            break
        print sibling.get_text(),
    print ""
"""

#for footnote in soup.find_all("font-size:7px" in style): #="font-family: THZHAN+TimesNewRomanPSMT; font-size:7px"): #SECTION 2 FOOTNOTES
#    print footnote
#    print footnote.get_text()


#o.write(text_html)


"""
print (soup.find("div", {"id": "results-list"}))                                   #<div id="results-list"></div>
    print (soup.find("div", {"id": "results-list"})).get_text()                        #""
    print (soup.find("div", {"id": "results-list"})).find("div", {"title": "Results"}) #None

    for date in soup.find_all("div"): #print all div content in parsed html
        print date

        frenchID = BeautifulSoup(idLoc.get_attribute('innerHTML'), 'lxml')

        for item in page_source.select('div.noticefield'):
        for title in item.select('div.span2.noticefieldheading'):
            for thing in title.get_text().encode('utf-8').replace('\n','').replace('\t',''), '\t',:
                c.write(thing)
        for answer in item.select('div.offset2.noticefieldvalue'):
            for thing in answer.get_text().encode('utf-8').replace('\n',';').replace('\t',''):
                c.write(thing)
            c.write('\n')


def get_report_links(file_name):
    soup = make_soup(file_name)
    count = 0 #count the number of links for debugging purposes
    for item in soup.find_all("div", {"style": "display:none;"}):
        count += 1
        print BASE_URL + ((item.get_text().splitlines()[3])[8:])
    print count, "URLS have been created"


#get_category_links returns the list of urls for the multiple category winners.
def get_category_links(section_url):
    soup = make_soup(section_url)
    boccat = soup.find("dl", "boccat")
    category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
    return category_links

#get_category_winner takes one category_url and deduces who the winners and runner-ups are based on similar webpage structure
def get_category_winner(category_url):
    soup = make_soup(category_url)
    category = soup.find("h1", "headline").string
    winner = [h2.string for h2 in soup.findAll("h2", "boc1")]
    runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]
    return {"category": category,
            "category_url": category_url,
            "winner": winner,
            "runners_up": runners_up}


for item in page_source.select('div.noticefield'):
        for title in item.select('div.span2.noticefieldheading'):
            for thing in title.get_text().encode('utf-8').replace('\n','').replace('\t',''), '\t',:
                c.write(thing)
                t.write(thing)
        for answer in item.select('div.offset2.noticefieldvalue'):
            for thing in answer.get_text().encode('utf-8').replace('\n','').replace('\t',''):
                c.write(thing)
                t.write(thing)
            c.write('\n')
            t.write('\n')
        #print item.get_text()


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
"""