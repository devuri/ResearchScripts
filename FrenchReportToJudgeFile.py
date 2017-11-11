# -*- coding: utf-8 -*-

"""
This program processes a folder of French court reports for judge names. The output file will have one line for each court report,
with judge names along with extraneous information in the line. The purpose of this program is to move the sentences containing
judge names from many files into one to simplify processing in another program (FrenchJudgeNames.py) that will then filter out
only the judge names.

KEY:
"président/president" = "president"
"greffier/greffière/greffièr" = "registrar"
"composée de" = "composed of"
"juges" = "judges"
"""


import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with location of folder to contains French court reports

#Location of Output File
JUDGES_FILE = '' #Fill in with location of file to contains judge names

j = open(JUDGES_FILE, 'w')

numFiles = 0
numJudges = 0
noJudge = []

#get/read all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    numFiles += 1

    index = 0
    foundJudges = False

    #no president in judge list
    if file in ["001-76017.txt","001-69699.txt","001-67320.txt","001-61803.txt","001-61801.txt","001-61607.txt","001-61608.txt","001-58857.txt","001-161247.txt","001-77516.txt"]:
        for line in lines:
            if not foundJudges:
                if "composée de" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    while not "greffière" in lines[index].lower() and not "greffier" in lines[index].lower() and not "greffièr" in lines[index].lower():
                        index += 1
                        j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
            index += 1

    #no registrar in judge list
    elif file in ["001-80854.txt","001-61463.txt"]:
        for line in lines:
            if not foundJudges:
                if "composée de" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    while not "juges" in lines[index].lower():
                        index += 1
                        j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
            index += 1

    else:
        #get each line in each file
        for line in lines:
           if not foundJudges:
               #president and registrar are in the same line
                if ("président" in lines[index].lower() or "president" in lines[index].lower()) and ("greffier" in lines[index].lower() or "greffière" in lines[index].lower() or "greffièr" in lines[index].lower() or "greffiier" in lines[index].lower() or "greffer" in lines[index].lower()):
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
                #"registrar" is in a subsequent line
                elif ("président" in lines[index].lower() or "president" in lines[index].lower()):
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    j.write(lines[index].replace('\n','').replace('\t',''))
                    presidentLine = index + 1
                    while presidentLine < len(lines) and not "greffier" in lines[presidentLine].lower() and not "greffière" in lines[presidentLine].lower() and not "greffièr" in lines[presidentLine].lower() and not "greffer" in lines[presidentLine].lower():
                        j.write(lines[presidentLine].replace('\n','').replace('\t',''))
                        presidentLine += 1
                    if presidentLine < len(lines):
                        j.write(lines[presidentLine].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1

                index += 1

    j.write('\n')

    if not foundJudges:
        noJudge.append(file)

j.close()

print numFiles
print numJudges
print noJudge
print len(noJudge)