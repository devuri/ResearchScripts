"""
There are two text files, one with the original URLs whose contents have been downloaded already and one with new URLs from
an updated search. However, there is some overlap in the two lists of URLs. We only want the completely new urls, so the program
only prints urls from the updated search not in the original URLs list.
"""

#Location of original URL File
URL_FILE = '' #Fill in

#u is the file that contains all the original urls
u = open(URL_FILE, 'r')
originalurlList = u.readlines()
u.close()

#Location of updated URL File
UPDATE_URL_FILE = '' #Fill in

#n is the file that contains all the update urls
n = open(UPDATE_URL_FILE, 'r')
updateurlList = n.readlines()
n.close()


for newurl in updateurlList:
    match = False
    for oldurl in originalurlList:
        if newurl.strip('\n') == oldurl.strip('\n'):
            match = True
    if not match: #if the newurl is not in originalurlList
        print newurl,
