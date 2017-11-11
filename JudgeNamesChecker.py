# -*- coding: utf-8 -*-

#This program checks to make sure we have judge names for all the full judgments and that we have the text file
#for each itemid from the judge names list.

import glob, os


#Location of file containing all the judge names. Each line is a full judgment itemid, a tabspace, and then a single judge name.
JUDGE_NAME_FILE = '' #Fill in (text file)

#Location of directory containing English full judgments (11447 files)
FULL_JUDGMENTS_FILES_ENGLISH = '' #Fill in (folder)

#Location of directory containing French full judgments (7523 files)
FULL_JUDGMENTS_FILES_FRENCH = '' #Fill in (folder)


#textFileItemidList is a list of itemids that correspond to full judgment text files in the two folders above
textFileItemidList = []

#judgeNamesItemidList is a list of itemids that correspond to full judgments for which we have judge names
judgeNamesItemidList = []


#add to textFileItemidList the itemid of every English judgment for which we have a text file
os.chdir(FULL_JUDGMENTS_FILES_ENGLISH)
for file in glob.glob("*.txt"):
    itemid = file.replace('.txt','').replace('.','-')
    textFileItemidList.append(itemid)

#add to textFileItemidList the itemid of every French judgment for which we have a text file
os.chdir(FULL_JUDGMENTS_FILES_FRENCH)
for file in glob.glob("*.txt"):
    itemid = file.replace('.txt','').replace('.','-')
    textFileItemidList.append(itemid)


#Read all the lines from JUDGE_NAME_FILE, one line for each judge name
n = open(JUDGE_NAME_FILE,'r')
judgeLines = n.readlines()
n.close()

#add to judgeNamesItemidList the itemid of each line in the JUDGE_NAME_FILE text file
for line in judgeLines:
    itemid = line.strip('\n').split('\t')[0] #itemid comes before the tabspace for each line
    if not itemid in judgeNamesItemidList[-1:]: #itemid is not the same as the previous itemid (so a new itemid)
        judgeNamesItemidList.append(itemid)

#Find itemids for which we have judge names but no text files - should only print for 001-163224
for itemid in judgeNamesItemidList:
    if not itemid in textFileItemidList:
        print "We have the judge names but no text file for itemid",itemid

#Find itemids for which we have text files but no judge names
for itemid in textFileItemidList:
    if not itemid in judgeNamesItemidList:
        print "We have the text file but no judge names for itemid", itemid