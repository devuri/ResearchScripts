"""
This program parses a local html file containing the "hidden" HTML from the HUDOC search results page and extracts
the itemids of the searched reports to create a list of urls for individual court reports.

In order to extract the "hidden" html code (containing itemids):
    Make sure to scroll all the way down the page so you can get all the links
        (We can reach ~1400 reports in a minute of scrolling)
    Go back up to the top of the page
    Right click the first link, and click "Inspect" on the drop down menu
    Navigate from top of html code:
        <body> ; <div id="main content"> ; <div id="inner-content"> ;
        <div class="row"> ; <div class="span12 results-container"> ;
        <div id="results-list"> ; <div title="Results"> ; <div class="results-list-block ">
    Then right click on the line that contains "results-list-block " -> Copy -> Copy OuterHTML
    Then Paste into a Text Wrangler text file to save HTML code
"""


#import statements
from bs4 import BeautifulSoup

#BASE_URL is the prefix for urls leading to individual court reports
BASE_URL = "http://hudoc.echr.coe.int/eng?i=" #+item id

#HOME_FILE is the location of the local html file
HOME_FILE = "" #Fill in

#helper function to get html code from file in lxml soup format
def make_soup(file_name):
    with open(file_name, 'r') as openfh:
        soup = BeautifulSoup(openfh, 'lxml')
    return soup

#get_report_links prints out the urls of the individual court reports
def get_report_links(file_name):
    soup = make_soup(file_name)
    count = 0 #count the number of links for debugging purposes
    for item in soup.find_all("div", {"style": "display:none;"}):
        count += 1
        print BASE_URL + ((item.get_text().splitlines()[3])[8:])
    print count, "URLS have been created"


#main
if __name__ == '__main__':
    get_report_links(HOME_FILE)