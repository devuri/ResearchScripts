# -*- coding: utf-8 -*-

"""
This program parses the HTML UN Session reports for Section 1 sponsorship data.
"""

#CONSTANTS - CHANGE THESE FOR DIFFERENT SESSIONS
UN_SESSION_NUMBER = 57
keyExpression = "font-family: PVQCKM+AbadiMT-CondensedLight; font-size:10px" #indicate sponsorship
#"font-family: IZWLWX+AbadiMT-CondensedLight; font-size:10px" #Session 57 Section 1
#"font-family: PVQCKM+AbadiMT-CondensedLight; font-size:10px" #Session 57 Section 6
#"font-family: VILBJN+ArialNarrow; font-size:12px" #Session 58 Section 1
#"font-family: VBMHAC+ArialNarrow; font-size:12px" #Session 58 Section 6
#"font-family: YFYRAR+ArialNarrow; font-size:12px" #Session 59 Section 1
#"font-family: BPWPOL+ArialNarrow; font-size:12px" #Session 59 Section 6
#"font-family: MHEVTX+ArialNarrow; font-size:12px" #Session 60 Section 1
#"font-family: CSECMQ+ArialNarrow; font-size:12px" #Session 60 Section 6
#"font-family: UBKKMU+ArialNarrow; font-size:12px" #Session 61 Section 1
#"font-family: EHISMP+ArialNarrow; font-size:12px" #Session 61 Section 6
#"font-family: BIRFCM+Arial; font-size:11px"     #Session 62 Section 1
#"font-family: RLJIIZ+Arial; font-size:11px"     #Session 62 Section 6
#"font-family: GVNGYF+Arial; font-size:11px"     #Session 63 Section 1
#"font-family: GJWZGU+Arial; font-size:11px"     #Session 63 Section 6
#"font-family: BOPVUT+Arial; font-size:11px"     #Session 64 Section 1
#"font-family: HUCRVE+Arial; font-size:11px"     #Session 64 Section 6
#"font-family: HJQVXL+Arial; font-size:11px"     #Session 66 Section 1
#"font-family: CTYHRW+Arial; font-size:11px"     #Session 66 Section 6
#"font-family: HAGRWU+Helvetica; font-size:13px" #Session 67 Section 1
#"font-family: YOTGFM+Helvetica; font-size:13px" #Session 67 Section 6
#"font-family: PJPRMV+Helvetica; font-size:13px" #Session 68 Section 1
#"font-family: FGYNND+Helvetica; font-size:13px" #Session 68 Section 6
#"font-family: RLSDWZ+Helvetica; font-size:13px" #Session 69 Section 1
#"font-family: ZCISNN+Helvetica; font-size:13px" #Session 69 Section 6
#"font-family: EQGQCQ+ArialMT; font-size:11px","font-family: YMYTFJ+ArialMT; font-size:11px" #Session 70 Section 1
#"font-family: MIKAAR+ArialMT; font-size:11px"   #Session 70 Section 6
voteExpression = "font-family: ZWHFQA+ArialNarrow-Italic; font-size:12px"
#"font-family: ZWHFQA+ArialNarrow-Italic; font-size:12px" #Session 58 Section 1
#"font-family: FLPXMN+ArialNarrow-Italic; font-size:12px" #Session 59 Section 1
#"font-family: KJVBJO+ArialNarrow-Italic; font-size:12px" #Session 60 Section 1
#"font-family: YTIGPM+ArialNarrow-Italic; font-size:12px" #Session 61 Section 1
#"font-family: XJBEOY+ArialNarrow-Italic; font-size:12px" #Session 61 Section 6
#"font-family: KGOHHO+Arial,Italic; font-size:11px"      #Session 62 Section 1
#"font-family: EEUWGB+Arial,Italic; font-size:11px"      #Session 62 Section 6
#"font-family: AIUJKB+Arial,Italic; font-size:11px"      #Session 63 Section 1
#"font-family: FSHMOV+Arial,Italic; font-size:11px"      #Session 64 Section 1
#"font-family: SVXIGQ+Arial; font-size:11px"             #Session 66 Section 1
#"font-family: HLBREU+Helvetica-Oblique; font-size:13px" #Session 67 Section 1
#"font-family: NXTPYW+Helvetica-Oblique; font-size:13px" #Session 67 Section 6
#"font-family: EGVVUF+Helvetica-Oblique; font-size:13px" #Session 68 Section 1
#"font-family: NQMDYP+Helvetica-Oblique; font-size:13px" #Session 69 Section 1
#"font-family: DFLCQA+Arial-ItalicMT; font-size:11px"    #Session 70 Section 1

#import statements
from bs4 import BeautifulSoup
import re
import xlwt

#Location of HTML File
HTML_FILE = "/Users/dongpengxia/Documents/UNGA/UNGASessionReports/TextHTML/%d.html" %UN_SESSION_NUMBER

e = open(HTML_FILE, 'r')
soup = BeautifulSoup(e, 'lxml') #parse page HTML with BeautifulSoup
e.close()

votesList = soup.find_all(style=voteExpression) #voting info can be same font but should not be in lists
sponsorsList = soup.find_all(style=keyExpression) #we want to filter sponsors out by font
for sponsors in sponsorsList:
    keepReading = True
    for sibling in sponsors.find_next_siblings():
        if sibling in votesList:
            keepReading = False #if we find a vote list in the sponsor list, we must delete that voting entry
        if not keepReading: #keepReading is false, there was a voting problem
            if sibling in sponsorsList:
                sponsorsList.remove(sibling)
    #next segment of code prints voting lists
    """
    if not keepReading:
        print "-------------------------------------------------------------------------------------------------------"
        for sibling in sponsors.find_next_siblings():
            print sibling
        print "-------------------------------------------------------------------------------------------------------"
    """

#continue cleaning sponsor lists
sponsorRecords = [] #list of sponsorship texts
newSponsorsList = [] #list of sponsorship HTML references
lastCopy = "ZZZZZ,ZZZZZ"
for sponsors in sponsorsList:
    currentCopy = sponsors.get_text()
    if currentCopy[:7] == "Adopted": #it's valid
        sponsorRecords.append(currentCopy)
        newSponsorsList.append(sponsors)
    else:
        #if current text is alphabetically after last text added to sponsorRecords
        if (len(currentCopy.split(',')) >= 2 and (currentCopy.strip('\n').strip(' ').strip(',').split(',')[0].strip(' ') > lastCopy.strip('\n').strip(' ').strip(',').split(',')[-1].strip(' '))):
            sponsorRecords[-1] = sponsorRecords[-1] + currentCopy
    if currentCopy[:7] == "Adopted":
        lastCopy = currentCopy
sponsorsList = newSponsorsList

"""
#For more recent sessions
#get resolution numbers
resolutionNumberList = []
for sponsors in sponsorsList:
    copy = sponsors
    searchStr = "A/RES/%d" %UN_SESSION_NUMBER
    while not searchStr in copy.get_text():
        copy = copy.find_previous()
    resolutionNumberList.append(copy.get_text())
"""

#"""
#For earlier sessions
#get resolution numbers
resolutionNumberList = []
for sponsors in sponsorsList:
    copy = sponsors
    searchStr = "RESOLUTION %d" %UN_SESSION_NUMBER
    while not searchStr in copy.get_text():
        copy = copy.find_previous()
    strToAdd = "A/RES/%d/" %UN_SESSION_NUMBER
    strToAdd += copy.get_text()[14:]
    resolutionNumberList.append(strToAdd)
#"""

#take out new line characters from sponsorRecords
for i in range(len(sponsorRecords)):
    sponsors = sponsorRecords[i]
    tempList = sponsors.split('\n')
    str = ""
    for temp in tempList:
        str = str + temp.strip('\n')
    sponsorRecords[i] = str

#start outputting content
if(len(sponsorRecords) == len(resolutionNumberList)):
    #Text-File Version
    SPONSOR_TAB_FILE = '' #Fill in with location of output text file
    t = open(SPONSOR_TAB_FILE, 'w')
    for i in range(len(resolutionNumberList)):
        t.write(resolutionNumberList[i].replace('\t',' ').replace('\n',' ').encode('utf-8'))
        t.write('\t')
        t.write(sponsorRecords[i].replace('\t',' ').replace('\n',' ').encode('utf-8'))
        t.write('\n')
    t.close()
    """
    #EXCEL Version
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Section 1")
    sheet.write(0,0,"Resolution #")
    sheet.write(0,1,"Sponsorship List")
    row = 1 #row is the row of the Excel spreadsheet that will be written next (starting at zero)
    for i in range(len(resolutionNumberList)):
        sheet.write(row,0,resolutionNumberList[row-1])
        sheet.write(row,1,sponsorRecords[row-1])
        row += 1
    workbook.save("/Users/dongpengxia/Downloads/Sponsorship%d.xls" %UN_SESSION_NUMBER)
    """
else:
    print "ERROR: The number of sponsors records and number of resolution numbers are not the same."
    print "# of sponsors records: ", len(sponsorRecords), len(sponsorsList)
    print "# of resolution numbers: ", len(resolutionNumberList)