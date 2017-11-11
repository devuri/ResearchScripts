"""
This program copies judgments that correspond to itemids in a list
"""

import os.path
from shutil import copyfile

ITEM_ID_FILE = "" #Fill in with location of text file with list of itemids
ORIGINAL_DIRECTORY = "" #Fill in with original location of case details
UPDATE_DIRECTORY = "" #Fill in with location of extra case details
COPY_DIRECTORY = "" #Fill in with location of destination folder of all files

#i is the file that contains the itemids
i = open(ITEM_ID_FILE, 'r')
itemIDList = i.readlines()
i.close()


count = 0
for itemid in itemIDList:
    itemid = itemid.strip('\n')
    itemid = itemid.strip(' ')
    newitemid = itemid + ".txt"
    itemid = itemid + ".txt" #remove or add \n before .txt in case this was an older folder

    if os.path.exists(ORIGINAL_DIRECTORY+itemid):
        copyfile(ORIGINAL_DIRECTORY+itemid, COPY_DIRECTORY+newitemid)
    else:
        if os.path.exists(UPDATE_DIRECTORY+itemid):
            copyfile(UPDATE_DIRECTORY+itemid, COPY_DIRECTORY+newitemid)
        else:
            #itemid does not exist in either directory
            print ("http://hudoc.echr.coe.int/eng?i=" + itemid[:-4])
    count += 1

print count