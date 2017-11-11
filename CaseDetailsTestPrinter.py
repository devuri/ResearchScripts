"""
This program demonstrates that the files GetCaseDetails.py writes can be parsed by '\t' to extract information to Excel
"""

#CASE_DETAILS is the location of a local text file produced by GetCaseDetails.py
CASE_DETAILS = '' #Fill in with location of case details text file

#c opens CASE_DETAILS for reading
c = open(CASE_DETAILS, 'r')

#linesList is a python list of the lines in file c
linesList = c.readlines()

#remove '\n' characters from list of lines, then parse by tab ('\t') characters into further lists
for line in linesList:
    print line.strip('\n').split('\t')
    #print contents in row format without spaces at the beginning and end
    #print line.strip('\n').split('\t')[0].strip(' ')
    #print line.strip('\n').split('\t')[1].strip(' ')