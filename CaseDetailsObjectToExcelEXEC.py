# -*- coding: utf-8 -*-

"""
This program processes a folder of case details files, makes case details dictionaries, then writes them to a file for excel usage.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with EXEC Case Details folder location

#categoryList is a list to store all the categories
#['Title', 'Description', 'Document Type', 'App Number', 'State', 'Language', 'Publication Date', 'Judgment Date',
# 'Final Judgment Date', 'CM Meeting Number', 'Supervision', 'Violations', 'ECHR Violations', 'Theme Domain',
# 'AP Status', 'Type', 'Leading Cases']

#Location of file to contain all the information in tabbed format
CASE_DETAILS_TAB_FILE = '' #Fill in with output file location


#t is the file to contain all the case reports in tabbed format
t = open(CASE_DETAILS_TAB_FILE, 'w')

#write category titles to file t
t.write('URL')
t.write('\t')
t.write('File Name')
t.write('\t')
t.write('Title')
t.write('\t')
t.write('Description')
t.write('\t')
t.write('Document Type')
t.write('\t')
t.write('App Number')
t.write('\t')
t.write('State')
t.write('\t')
t.write('Language')
t.write('\t')
t.write('Publication Date')
t.write('\t')
t.write('Judgment Date')
t.write('\t')
t.write('Final Judgment Date')
t.write('\t')
t.write('CM Meeting Number')
t.write('\t')
t.write('Supervision')
t.write('\t')
t.write('Violations')
t.write('\t')
t.write('ECHR Violations')
t.write('\t')
t.write('Theme Domain')
t.write('\t')
t.write('AP Status')
t.write('\t')
t.write('Type')
t.write('\t')
t.write('Leading Cases')
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()

    #caseReport is a dictionary to contain all the information from a file
    caseReport = {'Title':'', 'Description':'', 'Document Type':'', 'App Number':'', 'State':'', 'Language':'', 'Publication Date':'', 'Judgment Date':'', 'Final Judgment Date':'', 'CM Meeting Number':'', 'Supervision':'', 'Violations':'', 'ECHR Violations':'', 'Theme Domain':'', 'AP Status':'', 'Type':'', 'Leading Cases':''}

    #get each line in each file
    for line in lines:
        #category is the first item in a line split by tabs
        category = (line.strip('\n').split('\t'))[0]
        #information is the second item in a line split by tabs
        information = ((line.strip('\n').split('\t'))[1]).strip(';').replace('more…;;', '').replace('more…', '').replace(';;', ';')
        #update caseReport to include information from line
        caseReport[category] = information

    #add caseReport dictionary to file t
    t.write('http://hudoc.exec.coe.int/eng?i=')
    t.write(file[:-4].strip('\n'))
    t.write('\t')
    t.write(file[:-4].strip('\n'))
    t.write('\t')
    t.write(caseReport['Title'])
    t.write('\t')
    t.write(caseReport['Description'])
    t.write('\t')
    t.write(caseReport['Document Type'])
    t.write('\t')
    t.write(caseReport['App Number'])
    t.write('\t')
    t.write(caseReport['State'])
    t.write('\t')
    t.write(caseReport['Language'])
    t.write('\t')

    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Publication Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
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
    #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
    date = caseReport['Final Judgment Date'].split('/')
    if len(date) == 3:
        t.write(date[1])
        t.write('/')
        t.write(date[0])
        t.write('/')
        t.write(date[2])
        t.write('\t')
    else:
        t.write('\t')

    t.write(caseReport['CM Meeting Number'])
    t.write('\t')
    t.write(caseReport['Supervision'])
    t.write('\t')
    t.write(caseReport['Violations'])
    t.write('\t')
    t.write(caseReport['ECHR Violations'])
    t.write('\t')
    t.write(caseReport['Theme Domain'])
    t.write('\t')
    t.write(caseReport['AP Status'])
    t.write('\t')
    t.write(caseReport['Type'])
    t.write('\t')
    t.write(caseReport['Leading Cases'])
    t.write('\n')

    f.close()

t.close()