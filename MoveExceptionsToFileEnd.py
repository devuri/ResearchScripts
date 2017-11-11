"""
This program takes a file and prints out its contents with exception urls at the end.
"""

#Location of File
FILE = '' #Fill in with location of URL file

#f refers to the File opened for reading
f = open(FILE, 'r')

#linesList is a list of the lines in f
linesList = f.readlines()

#Location of File of Exceptions
EFILE = '' #Fill in with location of exceptions URL file

#e refers to a file containing a list of exception urls
e = open(EFILE, 'r')

#elinesList is a list of the lines in e
elinesList = e.readlines()


for line in linesList:
    match = False #match indicates if a line in the url file is also contained in the exception file
    for eline in elinesList:
        #if line is in both files
        if line.strip('\n') == eline.strip('\n'):
            match = True #update match to true if line is contained in both files
    if not match:
        print line, #if line is only in the url file, print the line

print "" #print new line
for eline in elinesList:
    print eline, #print all the exception urls at the end