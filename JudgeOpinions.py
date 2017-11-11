# -*- coding: utf-8 -*-

import unicodedata, glob, os

"""
This program gets dissenting and separate opinions from judges in the full judgments.
"""


#Location of file containing all the judge names. Each line is a full judgment itemid, a tabspace, and then a single judge name.
JUDGE_NAME_FILE = '' #Fill in

#Location of Output File
OUTPUT_FILE = '' #Fill in with location of output text file

#Location of directory containing English full judgments (11447 files)
FULL_JUDGMENTS_FILES = '' #Fill in


#Read all the lines from JUDGE_NAME_FILE, one line for each judge name
n = open(JUDGE_NAME_FILE,'r')
judgeLines = n.readlines()
n.close()

o = open(OUTPUT_FILE, 'w')
judgeLastNamesList = []

#caseList is a list of cases (1 case = 1 dictionary[itemid,[judges{name,dissenting opinion,separate opinion,concurring opinion}]])
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


    """
    #Manual Replacement: Error-Prone with uppercase and lowercase special characters
    judgeLastName = judgeLastName.lower()
    judgeLastName = judgeLastName.replace("ć","c").replace("ş","s").replace("č","c").replace("î","i").replace("ó","o").replace("ä","a")
    judgeLastName = judgeLastName.replace("ö","o").replace("Š","s").replace("ė","e").replace("è","e").replace("ß","b").replace("ø","o")
    judgeLastName = judgeLastName.replace("ă","a").replace("ț","t").replace("ū","u").replace("é","e").replace("β","b").replace("ü","u")
    judgeLastName = judgeLastName.replace("š","s").replace("á","a").replace("Ö","o").replace("Ü","u").replace("Á","a").replace("Í","i")
    judgeLastName = judgeLastName.replace("í","i").replace("É","e").replace("Ø","o").replace("Ä","a").replace("Ó","o").replace("ō","o")
    judgeLastName = judgeLastName.replace("ž","z").replace("Ţ","t").replace("Î","i").replace("ê","e").replace("Ş","s").replace("ű","u")
    judgeLastName = judgeLastName.replace("ő","o").replace("õ","o").replace("ž","z").replace("ı","i").replace("û","u").replace("ç","c")
    judgeLastName = judgeLastName.replace("Ć","c").replace("ń","n").replace("Ž","z").replace("ţ","t").replace("ċ","c")
    """


    if not judgeLastName in judgeLastNamesList:
        judgeLastNamesList.append(judgeLastName)

    #judgeProfile is a dictionary for a judge last name and whether a dissenting,separate,and/or concurring opinion was given
    judgeProfile = {'lastname':judgeLastName,'dissenting':-1,'separate':-1,'concur':-1}


    newItemid = True #flag for whether the line's itemid has been encountered yet
    if len(caseList) > 0: #if caseList is not empty
        case = caseList[-1] #case is the last item in caseList
        if itemid == case['itemid']: #if itemid is not for a new case
            newItemid = False
            case['judgelastnames'].append(judgeProfile) #add judge last name to case

    #if this line contains the first judge for a new court case
    if newItemid:
        newCaseDict = {'itemid':itemid, 'judgelastnames':[judgeProfile]} #start a new dictionary (for the new case) to add to the list
        caseList.append(newCaseDict)


    #o.write(judgeLastName)
    #o.write('\n')
#o.close()



#display a list of unique judge last names
#for name in judgeLastNamesList:
#    print name


#18971 cases
#print len(caseList)





#go through each court case one by one
for case in caseList:
    file_path = FULL_JUDGMENTS_FILES + case['itemid'].replace('-','.') + '.txt'
    if os.path.isfile(file_path):
        f = open(file_path,'r')
        lines = f.readlines()
        f.close()

        #add one to each field to show that the judge's case has been read
        for judge in case['judgelastnames']:
            judge['dissenting'] += 1
            judge['separate'] += 1
            judge['concur'] += 1


        #If all the lines are less than 100 characters, add up the text and split up sentences by periods
        allLineLengthU100 = True
        for line in lines:
            if len(line) > 100:
                allLineLengthU100 = False
        if allLineLengthU100:
            str = ""
            for line in lines:
                str = str + line.replace('\n',' ')
            lines = str.split('.')

        #go through each line looking for "dissent" and "separate" to tick off judge opinions
        for line in lines:
            #"convert" line to English characters only
            #originalLine = line
            line = unicode(line,'utf-8')
            line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
            line = line.lower()


            if "dissent" in line:# and "opinion" in line:
                #o.write(case['itemid'])
                #o.write('\t')
                #o.write(originalLine.strip('\n'))
                #o.write('\n')
                for judge in case['judgelastnames']:
                    if judge['lastname'] in line:
                        judge['dissenting'] += 1
            if "separate " in line:# and "opinion" in line:
                for judge in case['judgelastnames']:
                    if judge['lastname'] in line:
                        judge['separate'] += 1
            if "concur" in line:# and "opinion" in line:
                for judge in case['judgelastnames']:
                    if judge['lastname'] in line:
                        judge['concur'] += 1
            #if "vote" in line:


            #if "dissent" in line and not "opinion" in line:
            #    print line

        #for judge in case['judgelastnames']:
        #    if (judge['dissenting'] % 2 == 1 or judge['separate'] % 2 == 1):
        #        print case['itemid'],judge['lastname'],judge['dissenting'],judge['separate']




"""
#title line of judge opinions text file to spreadsheet
o.write('itemid')
o.write('\t')
o.write('judge last name')
o.write('\t')
o.write('"dissent"')
o.write('\t')
o.write('"separate "')
o.write('\t')
o.write('"concur"')
o.write('\n')


for case in caseList:
    for judge in case['judgelastnames']:
        o.write(case['itemid'])
        o.write('\t')
        o.write(judge['lastname'])
        o.write('\t')
        o.write('%d' % judge['dissenting'])
        o.write('\t')
        o.write('%d' % judge['separate'])
        o.write('\t')
        o.write('%d' % judge['concur'])
        o.write('\n')
"""

o.close()





"""
#go to folder that contains all the files
os.chdir(FULL_JUDGMENTS_FILES)

count = 0

number = 0

#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
"""

"""
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the following dissenting opinions are annexed to this judgment:
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the following dissenting opinions are annexed to this judgment:
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the following separate opinions are annexed to this judgment:
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the partly dissenting opinion of Mr Türmen is annexed to this judgment.
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the following separate opinions are annexed to this judgment:
    #In accordance with Article 45 § 2 of the Convention and Rule 74 § 2 of the Rules of Court, the following separate opinions are annexed to this judgment:
    #Judge A. ROSS, availing himself of his right under the terms of Rule 50 (2) of the Rules of Court, appends his dissenting opinion to the present judgment.
    #Judge G. Maridakis, availing himself of his right under the terms of Rule 50 (2) of the Rules of Court, annexes his dissenting opinion to the present judgment.
    #Mr. M. Zekia, Judge, considers that there was a breach of Article 5 (3) (art. 5-3) of the Convention; he attaches to the present judgment the statement of his dissenting opinion (Article 51 (2) of the Convention and Rule 50 (2) of the Rules of Court) (art. 51-2).
    #MM. A. Holmbäck and M. Zekia, Judges, consider that there was a breach of Article 6 (1) (art. 6-1) of the Convention as regards the length of the proceedings against the Applicant.  Availing themselves of the right under the terms of Article 51 (2) (art. 51-2) of the Convention and Rule 50 (2), of the Rules of Court, they annex their dissenting opinions to the present judgment.
    #MM. A. Holmbäck, G. Maridakis, E. Rodenbourg, A. Ross, T. Wold, G. Wiarda and A. Mast, Judges, considering that Section 7 (3) of the Act of 2nd August 1963 respects the Convention and the Protocol (cf. point I of the operative provisions of the judgment), avail themselves of the right under the terms of Article 51 (2) (art. 51-2) of the Convention and Rule 50 (2) of the Rules of Court: MM. Holmbäck, Rodenbourg, Ross, Wiarda and Mast, Judges, attach to the judgment the statement of their collective dissenting opinion: MM. Maridakis and Wold attach thereto the statement of their individual dissenting opinions.
    # 001-57513 ALERT: CONCURRING AND DISSENTING OPINIONS ALL INSIDE ONE LINE - in accordance with Article 51 para. 2 (art. 51-2) of the Convention and Rule 52 para. 2 of the Rules of Court, a concurring opinion of Mr. Cremona, a joint concurring opinion of Mrs. Bindschedler-Robert, Mr. Pinheiro Farinha, Mr. Pettiti, Mr. Walsh, Mr. Russo and Mr. Bernhardt and a partly dissenting opinion of Mr. Spielmann;
    """


"""
    ALERT: SENTENCE SPREAD OVER MULTIPLE LINES
        001-58058
        In accordance with Article 51 para. 2 of the Convention
        (art. 51-2) and Rule 55 para. 2 of Rules of Court B, the dissenting
        opinion of Mr Morenilla is annexed to this judgment.

        001-57439 A declaration by Mr Pinheiro Farinha is annexed to the present
        001-57481 annexed to this judgment:
        001-57483 opinions contained in the report is annexed to this judgment.
        001-57484 contained in the report is annexed to this judgment.
        001-57494 There are annexed to the present judgment:
        001-57513 There are annexed to the present judgment:
        001-57535 is annexed to this judgment.
        001-57576 A declaration by Mr. Thór Vilhjálmsson is annexed to the present judgment. #this one isn't even an opinion
        001-57625 by Mr Cremona is annexed to the present judgment.
        001-57632 is annexed to this judgment.
        001-57633 of Mr Ryssdal and Mr Pinheiro Farinha are annexed to this judgment.
        001-57639 annexed to the present judgment*.
        001-57649 the separate opinions contained in the report is annexed to the
        001-57673 Mr Matscher is annexed to this judgment.
        001-57728 annexed to the present judgment.
        001-57743 Mr Thór Vilhjálmsson, Mr Russo and Mr Valticos is annexed to the
        001-57748 separate opinions are annexed to this judgment:
        001-57756 opinion of Mr Bigi is annexed to the present judgment.
        001-57766 Mr Walsh, Mr Macdonald and Mrs Palm are annexed to this judgment.
        001-57780 dissenting opinion of Mr Walsh is annexed to this judgment.
        001-57788 Mr Russo, is annexed to this judgment.
        001-57793 annexed to this judgment.
        001-57938 dissenting opinion of Mr Gölcüklü is annexed to this judgment.
        001-57939 separate opinions are annexed to this judgment:
        001-57951 opinion of Mr Walsh is annexed to this judgment.
        001-57957 dissenting opinion of Mr Morenilla is annexed to this judgment.
        001-57969 annexed to this judgment.
        001-57981 separate opinions are annexed to this judgment:
        001-57982 separate opinions are annexed to this judgment:
        001-57995 Mr Spielmann and Mr Lopes Rocha is annexed to this judgment.
        001-58045 opinion of Mr Foighel is annexed to this judgment.
        001-58050 opinion of Mr Foighel is annexed to this judgment.
        001-58055 separate opinions are annexed to this judgment:
        001-58057 opinion of Mr Morenilla is annexed to this judgment.
        001-58058 opinion of Mr Morenilla is annexed to this judgment.
        001-58059 dissenting opinion of Mr Morenilla is annexed to this judgment.
    """

    #IDEA: Use a "checker" for subsequent lines - sometimes one line will have both concurring and dissenting opinions
    #for line in lines:
        #if "annexed" in line.lower() and not "article 45" in line.lower() and not "article 51" in line.lower() and not "rule 50" in line.lower() and not "rule 52" in line.lower():
        #    print file[:-4],line


"""
    foundStart = False
    for line in lines:
        #1595 article 45/rule 74 opinion introductions
        if "article 45" in line.lower() and ("rule 74" in line.lower() or "rules 74" in line.lower()):
            #print line
            number+= 1
            foundStart = True


    if not foundStart:
        for line in lines:
            if "rule 50" in line.lower() and ("avail" in line.lower() or "annex" in line.lower() or "alone" in line.lower()):# and "article 50" in line.lower():
                print line
    """


    #THE BELOW CODE SEGMENT DEMONSTRATES THE NUMBER OF JUDGMENTS WITH THE WORD "DISSENT" BUT NO DISSENTING OPINIONS
"""
    foundAnnex = False
    foundDissent = False
    for line in lines:
        if "annex" in line.lower():
            foundAnnex = True
        if "dissenting opinion" in line.lower():
            foundDissent = True
    if not foundAnnex and foundDissent:
        print file[:-4]
    """




    #foundDissent = False
    #for line in lines:
    #    if "dissent" in line.lower():# or "separate" in line.lower():
    #        foundDissent = True
    #if foundDissent:
    #    count += 1

#print count

#print number