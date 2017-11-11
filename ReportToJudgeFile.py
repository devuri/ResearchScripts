# -*- coding: utf-8 -*-

"""
This program processes a folder of court reports for judge names. The output file will have one line for each court report,
with judge names along with extraneous information in the line. The purpose of this program is to move the sentences containing
judge names from many files into one to simplify processing in another program (JudgeNames.py) that will then filter out only the judge names.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in


#Location of Output File
JUDGES_FILE = '' #Fill in with location of output text file

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

    #no president in judge list or "president" in lines preceding names of judges
    if file in ["001-98493\n.txt", "001-75888\n.txt", "001-66843\n.txt", "001-146044\n.txt", "001-146047\n.txt", "001-115621\n.txt", "001-58001\n.txt", "001-58744\n.txt", "001-83396\n.txt"]:
        for line in lines:
            if not foundJudges:
                if "composed of" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    while not "registrar" in lines[index].lower():
                        index += 1
                        j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
            index += 1

    #"president" in lines preceding names of judges, "composed of" in lines preceding the "composed of" before names of judges (too early)
    elif file in ["001-58085\n.txt"]:
        for line in lines:
            if not foundJudges:
                if "composed of the" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    while not "registrar" in lines[index].lower():
                        index += 1
                        j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
            index += 1

    #no registrar in judge list
    elif file in ["001-71615\n.txt","001-102766\n.txt"]:
        for line in lines:
            if not foundJudges:
                if "composed of" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    while not "judges" in lines[index].lower():
                        index += 1
                        j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
            index += 1
    elif int(file.replace(".txt","").strip('\n')[4:]) < 2000 or file in ["001-110210.txt","001-22200.txt","001-22634.txt","001-22635.txt","001-22368.txt","001-22646.txt","001-99748.txt","001-98636.txt","001-98460.txt","001-97733.txt","001-95594.txt","001-92969.txt","001-91560.txt","001-89036.txt","001-88266.txt","001-85960.txt","001-83568.txt","001-80880.txt","001-78692.txt","001-78674.txt","001-76932.txt","001-76253.txt","001-76060.txt","001-72683.txt","001-72411.txt","001-68772.txt","001-68533.txt","001-67704.txt","001-67328.txt","001-67092.txt","001-67093.txt","001-66754.txt","001-5627.txt","001-5631.txt","001-5634.txt","001-5638.txt","001-5641.txt","001-5642.txt","001-99998.txt","001-5643.txt","001-5645.txt","001-5646.txt","001-4821.txt","001-4578.txt","001-24073.txt","001-24074.txt","001-24071.txt","001-24069.txt","001-24015.txt","001-23927.txt","001-23886.txt","001-23836.txt","001-23828.txt","001-23730.txt","001-23703.txt","001-23688.txt","001-23654.txt","001-23564.txt","001-23539.txt","001-23475.txt","001-23450.txt","001-23429.txt","001-23407.txt","001-23372.txt","001-23262.txt","001-23191.txt","001-23082.txt","001-22927.txt","001-22923.txt","001-22882.txt","001-22757.txt","001-22668.txt","001-22591.txt","001-22586.txt","001-22369.txt","001-22199.txt","001-22197.txt","001-22152.txt","001-22131.txt","001-22047.txt","001-155182.txt","001-141196.txt","001-126835.txt"]:
        doNothing = True #do nothing
    else:
        #get each line in each file
        for line in lines:
           if not foundJudges:
                if "president" in lines[index].lower() and ("registrar" in lines[index].lower() or "registar" in lines[index].lower() or "regisrar" in lines[index].lower() or "regitrar" in lines[index].lower() or "regstrar" in lines[index].lower() or "rgistrar" in lines[index].lower() or "reistrar" in lines[index].lower() or "egistrar" in lines[index].lower()):
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
                elif "president" in lines[index].lower() and "jurisconsult" in lines[index].lower():
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    j.write(lines[index].replace('\n','').replace('\t',''))
                    foundJudges = True
                    numJudges += 1
                elif "president" in lines[index].lower(): #"registrar" and "jurisconsult" are in a subsequent line
                    j.write(file[:-4].strip('\n'))
                    j.write('\t')
                    j.write(lines[index].replace('\n','').replace('\t',''))

                    presidentLine = index + 1
                    while presidentLine < len(lines) and not "registrar" in lines[presidentLine].lower() and not "jurisconsult" in lines[presidentLine].lower() and not "egistrar" in lines[presidentLine].lower():
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