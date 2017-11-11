# -*- coding: utf-8 -*-

"""
This program processes a folder of voting details files then writes them to a file for excel usage.
"""

#'IRAN (ISLAMIC REPUBLIC OF)': words in parentheses not included in older resolutions
#'CABO VERDE': cape verde in older resolutions
#'BOLIVIA (PLURINATIONAL STATE OF)': words in parentheses not included in older resolutions

import glob, os

#go to folder that contains all the files
os.chdir("") #Fill in

#Location of output file to contain all the information in tabbed format
VOTING_TAB_FILE = '' #Fill in with location of output text file

#t is the file to contain all the voting details in tabbed format
t = open(VOTING_TAB_FILE, 'w')


countryList = ['AFGHANISTAN','ALBANIA','ALGERIA','ANDORRA','ANGOLA','ANTIGUA AND BARBUDA','ARGENTINA','ARMENIA',
                'AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS',
                'BELGIUM','BELIZE','BENIN','BHUTAN','BOLIVIA (PLURINATIONAL STATE OF)','BOSNIA AND HERZEGOVINA',
                'BOTSWANA','BRAZIL','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CABO VERDE','CAMBODIA',
                'CAMEROON','CANADA','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','COLOMBIA','COMOROS',
                'CONGO','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CYPRUS','CZECH REPUBLIC',
                "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",'DEMOCRATIC REPUBLIC OF THE CONGO','DENMARK','DJIBOUTI','DOMINICA',
                'DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA',
                'ETHIOPIA','FIJI','FINLAND','FRANCE','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GREECE',
                'GRENADA','GUATEMALA','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HONDURAS','HUNGARY','ICELAND',
                'INDIA','INDONESIA','IRAN (ISLAMIC REPUBLIC OF)','IRAQ','IRELAND','ISRAEL','ITALY','JAMAICA',
                'JAPAN','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI','KUWAIT','KYRGYZSTAN',
                "LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYA','LIECHTENSTEIN',
                'LITHUANIA','LUXEMBOURG','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA',
                'MARSHALL ISLANDS','MAURITANIA','MAURITIUS','MEXICO','MICRONESIA (FEDERATED STATES OF)','MONACO',
                'MONGOLIA','MONTENEGRO','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS',
                'NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NORWAY','OMAN','PAKISTAN','PALAU','PANAMA',
                'PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','POLAND','PORTUGAL','QATAR','REPUBLIC OF KOREA',
                'REPUBLIC OF MOLDOVA','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT KITTS AND NEVIS','SAINT LUCIA',
                'SAINT VINCENT AND THE GRENADINES','SAMOA','SAN MARINO','SAO TOME AND PRINCIPE','SAUDI ARABIA','SENEGAL',
                'SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA',
                'SOUTH AFRICA','SOUTH SUDAN','SPAIN','SRI LANKA','SUDAN','SURINAME','SWAZILAND','SWEDEN',
                'SWITZERLAND','SYRIAN ARAB REPUBLIC','TAJIKISTAN','THAILAND','THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA',
                'TIMOR-LESTE','TOGO','TONGA','TRINIDAD AND TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TUVALU',
                'UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED REPUBLIC OF TANZANIA','UNITED STATES',
                'URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA (BOLIVARIAN REPUBLIC OF)','VIET NAM','YEMEN','ZAMBIA','ZIMBABWE']

#Write title line with country names
t.write("UN Resolution Number")
for name in countryList:
    t.write("\t")
    t.write(name)
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"): #for each resolution
    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    #write UN Resolution Number at beginning of line
    t.write(file[:-4].replace('\\','/'))

    #voteList is an empty parallel list to record country votes
    voteList = []
    for i in range(len(countryList)):
        voteList.append("")

    for line in lines:
        line = line.replace('\n','')
        voteCode = "" #voteCode tells what a country votes (Yes, No, Abstain, Absent)
        if line != "": #if the line isn't blank
            if line[:2] == "Y " or line[:2] == "y ":
                #print "YES"
                countryName = line[2:]
                voteCode = "1"
            elif line[:2] == "N ":
                #print "NO"
                countryName = line[2:]
                voteCode = "3"
            elif line[:2] == "A ":
                #print "ABSTAIN"
                countryName = line[2:]
                voteCode = "2"
            else:
                #print "ABSENT"
                countryName = line
                voteCode = "8"

            found = False #found is a flag for whether countryName is in the countryList
            index = 0
            for country in countryList:
                if countryName == country:
                    voteList[index] = voteCode
                    found = True
                index += 1
            if not found:
                print line, "not found"

    index = 0
    for country in countryList: #make certain the numbers line up between countryList and voteList
        t.write('\t')
        t.write(voteList[index])
        index += 1
    t.write('\n')

t.close()