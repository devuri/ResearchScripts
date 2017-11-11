# -*- coding: utf-8 -*-

"""
This program processes a folder of UN resolutions files, makes resolutions dictionaries, then writes them to a file for excel usage.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with resolutions details folder

#categoryList is a list to store all the categories
#categoryList = ['UN Resolution Symbol:', 'Link To:', 'Meeting Symbol:', 'Title:', 'Related Document:', 'Vote Notes:', 'Voting Summary:', 'Vote Date:', 'Agenda Information:']


#Location of file to contain all the information in tabbed format
RESOLUTIONS_TAB_FILE = '' #Fill in with location of output text file


#t is the file to contain all the resolution information in tabbed format
t = open(RESOLUTIONS_TAB_FILE, 'w')

#write category titles to file t
t.write('UN Resolution Symbol')
t.write('\t')
t.write('Link To')
t.write('\t')
t.write('Meeting Symbol')
t.write('\t')
t.write('Title')
t.write('\t')
t.write('Related Document')
t.write('\t')
t.write('Vote Notes')
t.write('\t')
t.write('Voting Summary')
t.write('\t')
t.write('Vote Date')
t.write('\t')
t.write('Agenda Information')
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    #caseReport is a dictionary to contain all the information from a file
    caseReport = {'UN Resolution Symbol:':'', 'Link To:':'', 'Meeting Symbol:':'', 'Title:':'', 'Related Document:':'', 'Vote Notes:':'', 'Voting Summary:':'', 'Vote Date:':'', 'Agenda Information:':''}

    #get each line in each file
    for line in lines:
        #category is the first item in a line split by tabs
        category = (line.strip('\n').split('\t'))[0]
        #information is the second item in a line split by tabs
        information = ((line.strip('\n').split('\t'))[1]).strip(';').replace(';;', ';')
        #update caseReport to include information from line
        caseReport[category] = information

    #add caseReport dictionary to file t
    t.write(caseReport['UN Resolution Symbol:'])
    t.write('\t')
    t.write(caseReport['Link To:'])
    t.write('\t')
    t.write(caseReport['Meeting Symbol:'])
    t.write('\t')
    t.write(caseReport['Title:'])
    t.write('\t')
    t.write(caseReport['Related Document:'])
    t.write('\t')
    t.write(caseReport['Vote Notes:'])
    t.write('\t')
    t.write(caseReport['Voting Summary:'])
    t.write('\t')


    #write in mm/dd/yyyy format
    t.write((caseReport['Vote Date:'])[4:6])
    t.write('/')
    t.write((caseReport['Vote Date:'])[6:8])
    t.write('/')
    t.write((caseReport['Vote Date:'])[:4])


    t.write('\t')
    t.write(caseReport['Agenda Information:'])
    t.write('\n')

t.close()