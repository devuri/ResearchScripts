"""
This program processes a folder of case details files and produces a list of categories.
"""

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in with folder of case details files

#categoryList is a list to store all the categories
categoryList = []

#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    #get each line in each file
    for line in lines:
        #category is the first item in a line split by tabs
        category = (line.strip('\n').split('\t'))[0]
        #if category is not already in categoryList, add it to categoryList
        if not (category in categoryList):
            categoryList.append(category)

print categoryList

#categoryList =
#['Originating Body', 'Document Type', 'Language(s)', 'Title', 'App. No(s).', 'Importance Level', 'Represented by',
# 'Respondent State(s)', 'Judgment Date', 'Conclusion(s)', 'Article(s)', 'Separate Opinion(s)', 'Domestic Law',
# 'Strasbourg Case-Law', 'Keywords', 'ECLI', 'Rules of Court', 'Applicability', 'International Law', 'Published in',
# 'Reference Date', 'Introduction Date']

#['Originating Body', 'Document Type', 'Language(s)', 'Title', 'Resolution No.', 'App. No(s).', 'Importance Level',
# 'Respondent State(s)', 'Resolution Date', 'Judgment Date', 'Conclusion(s)', 'Meeting Number', 'Report Date',
# 'Keywords', 'Strasbourg Case-Law', 'Represented by', 'Reference Date', 'Domestic Law', 'International Law',
# 'Rules of Court', 'Introduction Date']

#['Originating Body', 'Document Type', 'Language(s)', 'Title', 'App. No(s).', 'Importance Level', 'Represented by',
# 'Respondent State(s)', 'Decision Date', 'Conclusion(s)', 'Article(s)', 'Separate Opinion(s)', 'Domestic Law',
# 'Strasbourg Case-Law', 'Keywords', 'ECLI', 'Rules of Court', 'Applicability', 'International Law', 'Published in',
# 'Reference Date', 'Introduction Date']

#['Title', 'Description', 'Document Type', 'App Number', 'State', 'Language', 'Publication Date', 'Judgment Date',
# 'Final Judgment Date', 'CM Meeting Number', 'Supervision', 'Violations', 'ECHR Violations', 'Theme Domain',
# 'AP Status', 'Type', 'Leading Cases']

