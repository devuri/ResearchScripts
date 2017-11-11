# -*- coding: utf-8 -*-

"""
This program reads case details files, gets the applicant name from the title field, and then searches through
the reports to get the prefix behind the applicant's name, giving the applicant's gender.
"""

import glob, os, unicodedata

#go to folder that contains all the case details files
os.chdir("") #Fill in

#Folder containing all the full judgment texts
FULL_JUDGMENTS_FOLDER = "" #Fill in

#categoryList is a list to store all the categories
#categoryList = ['Originating Body', 'Document Type', 'Language(s)', 'Title', 'App. No(s).', 'Importance Level', 'Represented by', 'Respondent State(s)', 'Judgment Date', 'Conclusion(s)', 'Article(s)', 'Separate Opinion(s)', 'Domestic Law', 'Strasbourg Case-Law', 'Keywords', 'ECLI', 'Rules of Court', 'Applicability', 'International Law', 'Published in', 'Reference Date', 'Introduction Date']


#Location of file to contain all the information in tabbed format
CASE_DETAILS_TAB_FILE = '' #Fill in with location of output text file


#t is the file to contain all the case reports in tabbed format
t = open(CASE_DETAILS_TAB_FILE, 'w')

#write category titles to file t
t.write('URL')
t.write('\t')
t.write('File Name')
t.write('\t')
t.write('Originating Body')
t.write('\t')
t.write('Document Type')
t.write('\t')
t.write('Language(s)')
t.write('\t')
t.write('Title')
t.write('\t')
t.write('App. No(s).')
t.write('\t')
t.write('Importance Level')
t.write('\t')
t.write('Represented by')
t.write('\t')
t.write('Respondent State(s)')
t.write('\t')
t.write('Judgment Date')
t.write('\t')
t.write('Conclusion(s)')
t.write('\t')
t.write('Article(s)')
t.write('\t')
t.write('Separate Opinion(s)')
t.write('\t')
t.write('Domestic Law')
t.write('\t')
t.write('Strasbourg Case-Law')
t.write('\t')
t.write('Keywords')
t.write('\t')
t.write('ECLI')
t.write('\t')
t.write('Rules of Court')
t.write('\t')
t.write('Applicability')
t.write('\t')
t.write('International Law')
t.write('\t')
t.write('Published in')
t.write('\t')
t.write('Reference Date')
t.write('\t')
t.write('Introduction Date')
t.write('\t')
t.write('Applicant Gender')
t.write('\t')
t.write('Applicant Description')
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"):
    if os.path.exists(FULL_JUDGMENTS_FOLDER+file):
        f = open(file, 'r')
        lines = f.readlines()
        f.close()

        #caseReport is a dictionary to contain all the information from a file
        caseReport = {'Originating Body':'', 'Document Type':'', 'Language(s)':'', 'Title':'', 'App. No(s).':'', 'Importance Level':'', 'Represented by':'', 'Respondent State(s)':'', 'Judgment Date':'', 'Conclusion(s)':'', 'Article(s)':'', 'Separate Opinion(s)':'', 'Domestic Law':'', 'Strasbourg Case-Law':'', 'Keywords':'', 'ECLI':'', 'Rules of Court':'', 'Applicability':'', 'International Law':'', 'Published in':'', 'Reference Date':'', 'Introduction Date':''}

        #get each line in each file
        for line in lines:
            #category is the first item in a line split by tabs
            category = (line.strip('\n').split('\t'))[0]
            #information is the second item in a line split by tabs
            information = ((line.strip('\n').split('\t'))[1]).strip(';').replace('more…;;', '').replace('more…', '').replace(';;', ';')
            #update caseReport to include information from line
            caseReport[category] = information

        itemid = file[:-4].strip('\n')

        applicantGender = "UNKNOWN"

        if len(caseReport['Title'].lower().split("v.")) == 2:
            applicantName = caseReport['Title'].lower().split("v.")[0]

            #"convert" applicantName to English
            applicantName = unicode(applicantName,'utf-8')
            applicantName = unicodedata.normalize('NFKD',applicantName).encode('ascii','ignore')
            applicantName = applicantName.lower()
            applicantName = applicantName.strip(' ')

            #check for multiple applicants in one case
            if "other" in applicantName:
                applicantGender = "MULTIPLE"
            elif " and " in applicantName:
                applicantGender = "MULTIPLE"
            else:
                #clean up applicant name to be last name only
                applicantName = applicantName.strip(' ')
                applicantName = applicantName.split(' ')[len(applicantName.split(' '))-1]
                applicantName = applicantName.strip('-')
                applicantName = applicantName.split('-')[len(applicantName.split('-'))-1]
                applicantName = applicantName.strip('‑')
                applicantName = applicantName.split('‑')[len(applicantName.split('‑'))-1]
                applicantName = applicantName.replace("’","'")
                applicantName = applicantName.strip("'")
                applicantName = applicantName.split("'")[len(applicantName.split("'"))-1]
                applicantName = applicantName.strip('.')
                applicantName = applicantName.split('.')[len(applicantName.split('.'))-1]

                if len(applicantName) <= 2:
                    applicantGender = "UNKNOWN" #cleaned up last name is too short to uniquely identify in full judgment
                else:
                    f = open(FULL_JUDGMENTS_FOLDER+itemid+".txt",'r')
                    judgmentLines = f.readlines()
                    f.close()

                    genderAssignmentCount = 0 #set to 0 for each applicant

                    for line in judgmentLines:
                        #"convert" lines to English
                        line = unicode(line,'utf-8')
                        line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
                        line = line.lower()
                        line = line.strip(' ')

                        #if applicantName in line
                        if len(line.split(applicantName)) >= 2:
                            for j in range(len(line.split(applicantName))-1):
                                subline = line.split(applicantName)[-2-j].strip(' ') #check each word subsequence before applicant last name
                                for i in range(4): #check last four words before last name
                                    if len(subline.split(' ')) > i:
                                        if subline.split(' ')[-1-i].strip('.') == "mr":
                                            if applicantGender != "MALE":
                                                applicantGender = "MALE"
                                                genderAssignmentCount+=1
                                        elif subline.split(' ')[-1-i].strip('.') == "mrs":
                                            if applicantGender != "FEMALE":
                                                applicantGender = "FEMALE"
                                                genderAssignmentCount+=1
                                        elif subline.split(' ')[-1-i].strip('.') == "ms":
                                            if applicantGender != "FEMALE":
                                                applicantGender = "FEMALE"
                                                genderAssignmentCount+=1
                    if genderAssignmentCount == 0:
                        applicantGender = "UNKNOWN"
                    elif genderAssignmentCount > 1: #too many gender assignments
                        #an estimated 70% (14/20) of these are multiple people
                        applicantGender = "LIKELY MULTIPLE"
        else:
            applicantGender = "UNKNOWN" #we don't know how many applicants there are because of at least two v.'s



        #reread full judgment
        f = open(FULL_JUDGMENTS_FOLDER+itemid+".txt",'r')
        judgmentLines = f.readlines()
        f.close()

        #Figure out remaining unknowns from the text
        if applicantGender == "UNKNOWN":
            for line in judgmentLines:
                #"convert" lines to English
                line = unicode(line,'utf-8')
                line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
                line = line.lower()
                line = line.strip(' ')

                if "the applicant," in line:
                    genderTitle = line.split("the applicant,")[1].strip(' ').split(' ')[0].strip(' ').strip('.')
                    if genderTitle == "mr":
                        applicantGender = "MALE"
                    elif genderTitle == "mrs":
                        applicantGender = "FEMALE"
                    elif genderTitle == "ms":
                        applicantGender = "FEMALE"
                if "the applicants," in line:
                    genderTitle = line.split("the applicants,")[1].strip(' ').split(' ')[0].strip(' ').strip('.')
                    if genderTitle == "mr":
                        applicantGender = "MALE"
                    elif genderTitle == "mrs":
                        applicantGender = "FEMALE"
                    elif genderTitle == "ms":
                        applicantGender = "FEMALE"

        #Figure out remaining unknowns from the text (continued)
        if applicantGender == "UNKNOWN":
            for line in judgmentLines:
                #"convert" lines to English
                line = unicode(line,'utf-8')
                line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
                line = line.lower()
                line = line.strip(' ')

                if "the application was lodged by" in line:
                    line = line.split("the application was lodged by")[1].split('.')[0]
                    for genderTitle in line.strip(' ').split(' '):
                        genderTitle = genderTitle.strip(' ').strip('.')
                        if genderTitle == "mr":
                            applicantGender = "MALE"
                        elif genderTitle == "mrs":
                            applicantGender = "FEMALE"
                        elif genderTitle == "ms":
                            applicantGender = "FEMALE"
                if "the applications were lodged by" in line:
                    line = line.split("the applications were lodged by")[1].split('.')[0]
                    for genderTitle in line.strip(' ').split(' '):
                        genderTitle = genderTitle.strip(' ').strip('.')
                        if genderTitle == "mr":
                            applicantGender = "MALE"
                        elif genderTitle == "mrs":
                            applicantGender = "FEMALE"
                        elif genderTitle == "ms":
                            applicantGender = "FEMALE"

        #Figure out remaining unknowns from the text (continued for organizations)
        if applicantGender == "UNKNOWN":
            for line in judgmentLines:
                #"convert" lines to English
                line = unicode(line,'utf-8')
                line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
                line = line.lower()
                line = line.strip(' ')

                if "the applicant company" in line: #guaranteed
                    applicantGender = "ORGANIZATION"

                keyTextList = ["the application was lodged by", "the applicant,", "the applicants,", "the applicant company"]
                for keyText in keyTextList:
                    if keyText in line:
                        line = line.split(keyText)[1].strip(' ')
                        if "company" in line or "organisation" in line or "bank" in line or "political party" in line or "association" in line:
                            applicantGender = "ORGANIZATION"

        if applicantGender == "UNKNOWN" and "other" in caseReport['Title'].lower():
            applicantGender = "MULTIPLE"

        #DEBUGGING
        #if applicantGender == "UNKNOWN":
        #    print itemid
        #    print applicantGender



        #Get applicant description/informational text
        applicantDescription = ""
        record = False

        numLinesRecorded = 0
        for line in judgmentLines:
            if record and numLinesRecorded > 1 and line.replace(' ','').replace('\n','').replace('\t','').isupper(): #stop recording at next all caps line
                record = False
            if "FACTS" in line:
                record = True
            if record:
                applicantDescription += line.replace('\t',' ').replace('\n',' ')
                numLinesRecorded += 1

        numLinesRecorded = 0
        if applicantDescription == "":
            record = False
            for line in judgmentLines:
                if record and numLinesRecorded > 1 and line.replace(' ','').replace('\n','').replace('\t','').isupper(): #stop recording at next all caps line
                    record = False
                if "PROCEDURE" in line:
                    record = True
                if record:
                    applicantDescription += line.replace('\t',' ').replace('\n',' ')
                    numLinesRecorded += 1

        if len(applicantDescription) > 32757:
            applicantDescription = applicantDescription[0:32756]

        #add caseReport dictionary to file t
        t.write('http://hudoc.echr.coe.int/eng?i=')
        t.write(itemid)
        t.write('\t')
        t.write(itemid)
        t.write('\t')
        t.write(caseReport['Originating Body'])
        t.write('\t')
        t.write(caseReport['Document Type'])
        t.write('\t')
        t.write(caseReport['Language(s)'])
        t.write('\t')
        t.write(caseReport['Title'])
        t.write('\t')
        t.write(caseReport['App. No(s).'])
        t.write('\t')
        t.write(caseReport['Importance Level'])
        t.write('\t')
        t.write(caseReport['Represented by'])
        t.write('\t')
        t.write(caseReport['Respondent State(s)'])
        t.write('\t')

        #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
        date = caseReport['Judgment Date'].split('/')
        if len(date) == 3:
            t.write(date[1])
            t.write('/')
            t.write(date[0])
            t.write('/')
            t.write(date[2])
            t.write('\t')
        else:
            t.write('\t')

        t.write(caseReport['Conclusion(s)'])
        t.write('\t')
        t.write(caseReport['Article(s)'])
        t.write('\t')
        t.write(caseReport['Separate Opinion(s)'])
        t.write('\t')
        t.write(caseReport['Domestic Law'])
        t.write('\t')
        t.write(caseReport['Strasbourg Case-Law'])
        t.write('\t')
        t.write(caseReport['Keywords'])
        t.write('\t')
        t.write(caseReport['ECLI'])
        t.write('\t')
        t.write(caseReport['Rules of Court'])
        t.write('\t')
        t.write(caseReport['Applicability'])
        t.write('\t')
        t.write(caseReport['International Law'])
        t.write('\t')
        t.write(caseReport['Published in'])
        t.write('\t')

        #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
        date = caseReport['Reference Date'].split('/')
        if len(date) == 3:
            t.write(date[1])
            t.write('/')
            t.write(date[0])
            t.write('/')
            t.write(date[2])
            t.write('\t')
        else:
            t.write('\t')

        #write date but reformat into American Date Format (mm/dd/yyyy instead of dd/mm/yyyy)
        date = caseReport['Introduction Date'].split('/')
        if len(date) == 3:
            t.write(date[1])
            t.write('/')
            t.write(date[0])
            t.write('/')
            t.write(date[2])
            t.write('\t')
        else:
            t.write('\t')

        t.write(applicantGender) #write Applicant Gender to file

        t.write('\t')
        t.write(applicantDescription)

        t.write('\n')

t.close()