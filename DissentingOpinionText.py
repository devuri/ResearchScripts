# -*- coding: utf-8 -*-

import unicodedata, glob, os, xlwt

"""
This program gets dissenting opinion text segments from the full judgments. It reads the full judgments lines in reverse
because dissenting opinions always come at the end.
"""

#Collect Judge Names
#------------------------------------------------------------------------------------------------------------------------------------------------
#Location of file containing all the judge names. Each line is a full judgment itemid, a tabspace, and then a single judge name.
JUDGE_NAME_FILE = '' #Fill in with location of judge names text file

#Read all the lines from JUDGE_NAME_FILE, one line for each judge name
n = open(JUDGE_NAME_FILE,'r')
judgeLines = n.readlines()
n.close()

#caseList is a list of cases (1 case = 1 dictionary[itemid,[judges{name,lastname}])
caseList = []

for line in judgeLines:
    line = line.strip('\n')
    itemid = line.split('\t')[0] #itemid comes before the tabspace for each line
    judgeName = line.split('\t')[1] #the judge's name comes after the tabspace for each line
    judgeName = judgeName.strip(' ')
    judgeLastName = judgeName.split(' ')[len(judgeName.split(' '))-1]
    judgeLastName = judgeLastName.strip('-')
    judgeLastName = judgeLastName.split('-')[len(judgeLastName.split('-'))-1]
    judgeLastName = judgeLastName.strip('‑')
    judgeLastName = judgeLastName.split('‑')[len(judgeLastName.split('‑'))-1]
    judgeLastName = judgeLastName.strip('.')
    judgeLastName = judgeLastName.split('.')[len(judgeLastName.split('.'))-1]
    judgeLastName = judgeLastName.replace("’","'")
    judgeLastName = judgeLastName.strip("'")
    judgeLastName = judgeLastName.split("'")[len(judgeLastName.split("'"))-1]
    judgeLastName = judgeLastName.replace("[1]",'')

    #"convert" judgeLastName to English
    judgeLastName = unicode(judgeLastName,'utf-8')
    judgeLastName = unicodedata.normalize('NFKD',judgeLastName).encode('ascii','ignore')
    judgeLastName = judgeLastName.lower()

    #judgeProfile is a dictionary for a judge's full name and standardized last name
    judgeProfile = {'name':judgeName,'lastname':judgeLastName}

    newItemid = True #flag for whether the line's itemid has been encountered yet
    if len(caseList) > 0: #if caseList is not empty
        case = caseList[-1] #case is the last item in caseList
        if itemid == case['itemid']: #if itemid is not for a new case
            newItemid = False
            case['judges'].append(judgeProfile) #add judge last name to case

    #if this line contains the first judge for a new court case
    if newItemid:
        newCaseDict = {'itemid':itemid, 'judges':[judgeProfile]} #start a new dictionary (for the new case) to add to the list
        caseList.append(newCaseDict)

dissentList = []
#------------------------------------------------------------------------------------------------------------------------------------------------


#Location of Output File
OUTPUT_FILE = '' #Fill in with location of output file

#Location of directory containing English full judgments (11447 files)
FULL_JUDGMENTS_FILES = '' #Fill in with location of English full judgments folder

o = open(OUTPUT_FILE, 'w')

#go to folder that contains all the files
os.chdir(FULL_JUDGMENTS_FILES)

count = 0
number = 0

#get all the text files
for file in glob.glob("*.txt"):
    itemid = file.replace('.txt','').replace('.','-').replace('\n','')
    #these itemids up to 001-98550 do not have the "done in english" or "done in french" flags but have no special opinions (all unanimous)
    #so we omit them from processing
    if not itemid in ['001-107022','001-156274','001-161051','001-57524','001-57886','001-75450','001-75511','001-89583','001-92999','001-98550','001-162211','001-61696']:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        #If all the lines are less than 125 characters, add up the text and split up sentences by periods
        allLineLengthU125 = True
        for line in lines:
            if len(line) > 125:
                allLineLengthU125 = False
        if allLineLengthU125:
            str = ""
            for line in lines:
                str = str + line.replace('\n',' ')
            lines = str.split('.')

        #reverse the list because dissenting opinions are always at the end
        lines.reverse()
        #foundConclusion is a flag for whether we have reached the conclusion yet (filter out previous info)
        foundConclusion = False
        #foundDissent is a flag for whether we found "dissent" in the text segment
        foundDissent = False

        #lineNum is the number of lines in the text segment before "done in english" or "done in french" is reached
        lineNum = 0

        #textSegments and textSegmentsAsc are parallel lists that store lines from the text segments
        textSegments = []
        textSegmentsAsc = []

        #go through each line
        for line in lines:
            lineNum += 1
            if foundConclusion: #break out of loop if we've found the conclusion and have read all dissenting opinions
                break

            line = line.strip('\n')
            #keep a copy of the original line
            originalLine = line
            #"convert" line to English characters only
            line = unicode(line,'utf-8')
            line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
            line = line.lower()

            textSegments.insert(0,originalLine) #insert originalLine to front of textSegments
            textSegmentsAsc.insert(0,line) #insert ASCII line to front of textSegmentsAsc

            if "dissent" in line:
                foundDissent = True

            #implies foundConclusion is False
            if "done in english" in line or "done in french" in line: #filter out all the text before dissenting opinions
                foundConclusion = True #we've found the conclusions section, so ignore the rest of the lines

        if not foundConclusion: #if input is correct, nothing should go through this if statement
            print file, "does not have 'done in english' or 'done in french' keyword"

        if foundDissent:
            index = 0
            processingAppendix = False
            #dissentingOpinion = "" #a string to store the dissenting opinion text
            o.write('********************************************************************************************************************************************************************************************************\n')
            o.write(itemid)
            o.write('\n')
            o.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')

            dissentNum = 0
            dissentProfile = {'itemid':'','judgeNames':'','judgeLastNames':'','dissentNum':-1,'dissentText':'','numJudges':-1}
            for line in textSegmentsAsc:
                if "APPENDIX" in textSegments[index] or "appendix" in line[:8] or ('annex' in line and len(line) < 20) or ('date of birth' in line and len(line) < 20) or "list of applicants" in line:
                    processingAppendix = True
                if processingAppendix and "dissent" in line:
                    processingAppendix = False
                if not processingAppendix:
                    #dissentingOpinion = dissentingOpinion + textSegments[index] + '\n' #longest one has 239756 characters, over the Excel limit of 32767 characters per cell
                    if "OPINION" in textSegments[index] or "STATEMENT" in textSegments[index] or "OPINON" in textSegments[index] or "OPIONION" in textSegments[index]:
                        o.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
                        if dissentProfile['dissentNum'] != -1:
                            dissentList.append(dissentProfile)
                        dissentProfile = {'itemid':'','judgeNames':'','judgeLastNames':'','dissentNum':-1,'dissentText':'','numJudges':-1}

                        for case in caseList:
                            if case['itemid'] == itemid:
                                if "dissent" in textSegmentsAsc[index]:
                                    dissentNum += 1

                                    dissentProfile = {'itemid':itemid,'judgeNames':'','judgeLastNames':'','dissentNum':dissentNum,'dissentText':'','numJudges':0}
                                    for judge in case['judges']:
                                        if judge['lastname'] in textSegmentsAsc[index] or ((index + 1) < len(textSegmentsAsc) and judge['lastname'] in textSegmentsAsc[index + 1]):
                                            dissentProfile['judgeNames'] = dissentProfile['judgeNames'] + judge['name'] + ", "
                                            dissentProfile['judgeLastNames'] = dissentProfile['judgeLastNames'] + judge['lastname'] + ", "
                                            dissentProfile['numJudges'] += 1
                                    dissentProfile['judgeLastNames'] = dissentProfile['judgeLastNames'].strip(' ').strip(',')
                                    dissentProfile['judgeNames'] = dissentProfile['judgeNames'].strip(' ').strip(',')

                                break #break out of for loop to stop searching

                    dissentProfile['dissentText'] = dissentProfile['dissentText'] + textSegments[index] + '\n'
                    o.write(textSegments[index])
                    o.write('\n')
                index += 1
            #append last dissenting opinion of full judgment
            if dissentProfile['dissentNum'] != -1:
                dissentList.append(dissentProfile)
            o.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
o.close()


workbook = xlwt.Workbook()
sheet = workbook.add_sheet("DissentingOpinions")
sheet.write(0,0,"itemid")
sheet.write(0,1,"dissent number")
sheet.write(0,2,"Judge Names")
sheet.write(0,3,"Judge Last Names")
sheet.write(0,4,"Number of Judges")
sheet.write(0,5,"Dissenting Opinion Text")
row = 1 #row is the row of the Excel spreadsheet that will be written next (starting at zero)

for dissentingOpinion in dissentList:
    sheet.write(row,0,dissentingOpinion['itemid'].decode("utf8"))
    sheet.write(row,1,dissentingOpinion['dissentNum'])
    sheet.write(row,2,dissentingOpinion['judgeNames'].decode("utf8"))
    sheet.write(row,3,dissentingOpinion['judgeLastNames'].decode("utf8"))
    sheet.write(row,4,dissentingOpinion['numJudges'])
    if len(dissentingOpinion['dissentText']) <= 32767:
        sheet.write(row,5,dissentingOpinion['dissentText'].decode("utf8"))
    else: #dissentingOpinion text is too big to fit in one cell
        sheet.write(row,5,"OVERFLOW - dissenting opinion has too many characters to fit in one cell, please see reference")
        """
        str = dissentingOpinion['dissentText']
        while len(str) > 32767:
            sheet.write(row,5,(str[:32767]).decode("utf8"))
            str = str[32767:]
            row += 1
        sheet.write(row,5,str.decode("utf8"))
        """
    row += 1
workbook.save("") #Fill in with location of output excel spreadsheet