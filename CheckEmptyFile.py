"""
This program processes a folder of text files and checks that none of them are empty.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with folder of text files

count = 0

#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    if lines == []:
        print file, ' is empty.'
        #print ('http://hudoc.echr.coe.int/eng?i=' + file[:-4].strip('\n'))
        #print ('http://hudoc.exec.coe.int/eng?i=' + file[:-4].strip('\n'))
    else:
        count += 1
    f.close()

print count, 'files are not empty.'