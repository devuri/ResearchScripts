# -*- coding: utf-8 -*-

import unicodedata, glob, os

"""
This program separates the judgments into parts.
"""

#Location of Output File
OUTPUT_FILE = '' #Fill in with location of output text file

#Location of directory containing English full judgments (11447 files)
FULL_JUDGMENTS_FILES = '' #Fill in

os.chdir(FULL_JUDGMENTS_FILES)

titleList = []
lawCount = 0
procedureCount = 0
factsCount = 0
conclusionCount = 0
allCount = 0
count = 0

#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    foundLaw = False
    foundProcedure = False
    foundFacts = False
    foundConclusion = False
    for line in lines:
        line = line.strip('\n')
        line = line.strip(' ')
        line = line.replace('.','')
        line = line.replace(',','')
        line = line.replace('\t','')
        if line.isupper():
            if not line in titleList:
                titleList.append(line)
        if line == "THE LAW":
            foundLaw = True
        if line == "PROCEDURE":
            foundProcedure = True
        if line == "THE FACTS":
            foundFacts = True
        if "FOR THESE REASONS" in line:
            foundConclusion = True
    f.close()
    if foundLaw:
        lawCount += 1
    if foundProcedure:
        procedureCount += 1
    if foundFacts:
        factsCount += 1
    if foundConclusion:
        conclusionCount += 1
    if foundLaw and foundProcedure and foundFacts and foundConclusion:
        allCount += 1
    count += 1

print titleList
print lawCount
print procedureCount
print factsCount
print conclusionCount
print allCount
print count