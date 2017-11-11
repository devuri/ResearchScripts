"""
This program takes a file and outputs all of its contents without blank lines.
"""

#Location of Files
FILE = '' #Fill in
OUTPUT_FILE = '' #Fill in with location of output text file

#f refers to the File opened for reading
f = open(FILE, 'r')

#linesList is a list of the lines in f
linesList = f.readlines()
f.close()

o = open(OUTPUT_FILE, 'w')

#only output lines that are not blank
for line in linesList:
    if line != '\n':
        o.write(line)
o.close()