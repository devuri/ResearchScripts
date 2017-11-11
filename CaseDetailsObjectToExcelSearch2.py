# -*- coding: utf-8 -*-

"""
This program processes a folder of case details files, makes case details dictionaries, then writes them to a file for excel usage.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with case details folder location

#categoryList is a list to store all the categories
#categoryList = ['Originating Body', 'Document Type', 'Language(s)', 'Title', 'Resolution No.', 'App. No(s).', 'Importance Level', 'Respondent State(s)', 'Resolution Date', 'Judgment Date', 'Conclusion(s)', 'Meeting Number', 'Report Date', 'Keywords', 'Strasbourg Case-Law', 'Represented by', 'Reference Date', 'Domestic Law', 'International Law', 'Rules of Court', 'Introduction Date']


#Location of file to contain all the information in tabbed format
CASE_DETAILS_TAB_FILE = '' #Fill in with output text file location


#t is the file to contain all the case reports in tabbed format
t = open(CASE_DETAILS_TAB_FILE, 'w')

#write category titles to file t
t.write('URL')
t.write('\t')
t.write('File Name')
t.write('\t')
t.write('Originating Body')
t.write('\t')
t.write('Document Type')
t.write('\t')
t.write('Language(s)')
t.write('\t')
t.write('Title')
t.write('\t')
t.write('Resolution No.')
t.write('\t')
t.write('App. No(s).')
t.write('\t')
t.write('Importance Level')
t.write('\t')
t.write('Respondent State(s)')
t.write('\t')
t.write('Resolution Date')
t.write('\t')
t.write('Judgment Date')
t.write('\t')
t.write('Conclusion(s)')
t.write('\t')
t.write('Meeting Number')
t.write('\t')
t.write('Report Date')
t.write('\t')
t.write('Keywords')
t.write('\t')
t.write('Strasbourg Case-Law')
t.write('\t')
t.write('Represented by')
t.write('\t')
t.write('Reference Date')
t.write('\t')
t.write('Domestic Law')
t.write('\t')
t.write('International Law')
t.write('\t')
t.write('Rules of Court')
t.write('\t')
t.write('Introduction Date')
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()

    #caseReport is a dictionary to contain all the information from a file
    caseReport = {'Originating Body':'', 'Document Type':'', 'Language(s)':'', 'Title':'', 'Resolution No.':'', 'App. No(s).':'', 'Importance Level':'', 'Respondent State(s)':'', 'Resolution Date':'', 'Judgment Date':'', 'Conclusion(s)':'', 'Meeting Number':'', 'Report Date':'', 'Keywords':'', 'Strasbourg Case-Law':'', 'Represented by':'', 'Reference Date':'', 'Domestic Law':'', 'International Law':'', 'Rules of Court':'', 'Introduction Date':''}

    #get each line in each file
    for line in lines:
        #category is the first item in a line split by tabs
        category = (line.strip('\n').split('\t'))[0]
        #information is the second item in a line split by tabs
        information = (line.strip('\n').split('\t'))[1].strip(';').replace('more…;;', '').replace('more…', '').replace(';;', ';')
        #update caseReport to include information from line
        caseReport[category] = information

    #add caseReport dictionary to file t
    t.write('http://hudoc.echr.coe.int/eng?i=')
    t.write(file[:-4].strip('\n'))
    t.write('\t')
    t.write(file[:-4].strip('\n'))
    t.write('\t')
    t.write(caseReport['Originating Body'])
    t.write('\t')
    t.write(caseReport['Document Type'])
    t.write('\t')
    t.write(caseReport['Language(s)'])
    t.write('\t')
    t.write(caseReport['Title'])
    t.write('\t')
    t.write(caseReport['Resolution No.'])
    t.write('\t')
    t.write(caseReport['App. No(s).'])
    t.write('\t')
    t.write(caseReport['Importance Level'])
    t.write('\t')
    t.write(caseReport['Respondent State(s)'])
    t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Resolution Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2].split(' ')[0]) #remove default hours
        t.write('\t')
    else:
        t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Judgment Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
        t.write('\t')
    else:
        t.write('\t')

    t.write(caseReport['Conclusion(s)'])
    t.write('\t')
    t.write(caseReport['Meeting Number'])
    t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Report Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
        t.write('\t')
    else:
        t.write('\t')

    t.write(caseReport['Keywords'])
    t.write('\t')
    t.write(caseReport['Strasbourg Case-Law'])
    t.write('\t')
    t.write(caseReport['Represented by'])
    t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Reference Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
        t.write('\t')
    else:
        t.write('\t')

    t.write(caseReport['Domestic Law'])
    t.write('\t')
    t.write(caseReport['International Law'])
    t.write('\t')
    t.write(caseReport['Rules of Court'])
    t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Introduction Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
        t.write('\t')
    else:
        t.write('\t')

    t.write('\n')

    f.close()

t.close()