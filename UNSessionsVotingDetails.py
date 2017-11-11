# -*- coding: utf-8 -*-

"""
This program processes a folder of voting details files then writes them to a file for excel usage.
"""

#'IRAN (ISLAMIC REPUBLIC OF)': words in parentheses not included in older resolutions
#'CABO VERDE': cape verde in older resolutions
#'BOLIVIA (PLURINATIONAL STATE OF)': words in parentheses not included in older resolutions

import glob, os

SESSION_NUM = 57

#go to folder that contains all the files
os.chdir("/Users/dongpengxia/Documents/UNGA/UNGASessionReports/SponsorshipTabFiles/%d/"%SESSION_NUM)

#Location of output file to contain all the information in tabbed format
VOTING_TAB_FILE = '/Users/dongpengxia/Downloads/voting_tab_file%d.txt'%SESSION_NUM

#t is the file to contain all the voting details in tabbed format
t = open(VOTING_TAB_FILE, 'w')


countryList = ['AFGHANISTAN','ALBANIA','ALGERIA','ANDORRA','ANGOLA','ANTIGUA AND BARBUDA','ARGENTINA','ARMENIA',
                'AUSTRALIA','AUSTRIA','AZERBAIJAN','BAHAMAS','BAHRAIN','BANGLADESH','BARBADOS','BELARUS',
                'BELGIUM','BELIZE','BENIN','BHUTAN','BOLIVIA','BOLIVIA (PLURINATIONAL STATE OF)','BOSNIA AND HERZEGOVINA',
                'BOTSWANA','BRAZIL','BRUNEI DARUSSALAM','BULGARIA','BURKINA FASO','BURUNDI','CABO VERDE','CAPE VERDE','CAMBODIA',
                'CAMEROON','CANADA','CENTRAL AFRICAN REPUBLIC','CHAD','CHILE','CHINA','COLOMBIA','COMOROS',
                'CONGO','COSTA RICA',"COTE D'IVOIRE",'CROATIA','CUBA','CYPRUS','CZECH REPUBLIC',
                "DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",'DEMOCRATIC REPUBLIC OF THE CONGO','DENMARK','DJIBOUTI','DOMINICA',
                'DOMINICAN REPUBLIC','ECUADOR','EGYPT','EL SALVADOR','EQUATORIAL GUINEA','ERITREA','ESTONIA',
                'ETHIOPIA','FIJI','FINLAND','FRANCE','GABON','GAMBIA','GEORGIA','GERMANY','GHANA','GREECE',
                'GRENADA','GUATEMALA','GUINEA','GUINEA-BISSAU','GUYANA','HAITI','HONDURAS','HUNGARY','ICELAND',
                'INDIA','INDONESIA','IRAN','IRAN (ISLAMIC REPUBLIC OF)','IRAQ','IRELAND','ISRAEL','ITALY','JAMAICA',
                'JAPAN','JORDAN','KAZAKHSTAN','KENYA','KIRIBATI','KUWAIT','KYRGYZSTAN',
                "LAO PEOPLE'S DEMOCRATIC REPUBLIC",'LATVIA','LEBANON','LESOTHO','LIBERIA','LIBYA','LIECHTENSTEIN',
                'LITHUANIA','LUXEMBOURG','MADAGASCAR','MALAWI','MALAYSIA','MALDIVES','MALI','MALTA',
                'MARSHALL ISLANDS','MAURITANIA','MAURITIUS','MEXICO','MICRONESIA (FEDERATED STATES OF)','MONACO',
                'MONGOLIA','MONTENEGRO','MOROCCO','MOZAMBIQUE','MYANMAR','NAMIBIA','NAURU','NEPAL','NETHERLANDS',
                'NEW ZEALAND','NICARAGUA','NIGER','NIGERIA','NORWAY','OMAN','PAKISTAN','PALAU','PALESTINE','PANAMA',
                'PAPUA NEW GUINEA','PARAGUAY','PERU','PHILIPPINES','POLAND','PORTUGAL','QATAR','REPUBLIC OF KOREA',
                'REPUBLIC OF MOLDOVA','ROMANIA','RUSSIAN FEDERATION','RWANDA','SAINT KITTS AND NEVIS','SAINT LUCIA',
                'SAINT VINCENT AND THE GRENADINES','SAMOA','SAN MARINO','SAO TOME AND PRINCIPE','SAUDI ARABIA','SENEGAL',
                'SERBIA','SEYCHELLES','SIERRA LEONE','SINGAPORE','SLOVAKIA','SLOVENIA','SOLOMON ISLANDS','SOMALIA',
                'SOUTH AFRICA','SOUTH SUDAN','SPAIN','SRI LANKA','SUDAN','SURINAME','SWAZILAND','SWEDEN',
                'SWITZERLAND','SYRIAN ARAB REPUBLIC','TAJIKISTAN','THAILAND','THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA',
                'TIMOR-LESTE','TOGO','TONGA','TRINIDAD AND TOBAGO','TUNISIA','TURKEY','TURKMENISTAN','TUVALU',
                'UGANDA','UKRAINE','UNITED ARAB EMIRATES','UNITED KINGDOM','UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND',
                'UNITED REPUBLIC OF TANZANIA','UNITED STATES','UNITED STATES OF AMERICA',
                'URUGUAY','UZBEKISTAN','VANUATU','VENEZUELA (BOLIVARIAN REPUBLIC OF)','VIET NAM','YEMEN','ZAMBIA','ZIMBABWE']

#Write title line with country names
t.write("UN Resolution Number")
for name in countryList:
    t.write("\t")
    t.write(name)
t.write('\n')


#get all the text files
for file in glob.glob("*.txt"):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()

    for line in lines: #for each resolution
        t.write(line.split('\t')[0]) #write UN Resolution Number at beginning of line
        t.write('\t')

        line = line.lower().replace(" ","")

        for country in countryList:
            if country == 'BOLIVIA':
                if "bolivia" in line and not "bolivia(plurinationalstateof)" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'CONGO':
                if "congo" in line and "democraticrepublicofthecongo" in line and len(line.split("congo")) > 2:
                    t.write("1")
                elif "congo" in line and not "democraticrepublicofthecongo" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'REPUBLIC OF KOREA':
                if "republicofkorea" in line and "democraticpeople'srepublicofkorea" in line and len(line.split("republicofkorea")) > 2:
                    t.write("1")
                elif "republicofkorea" in line and not "democraticpeople'srepublicofkorea" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'DOMINICA':
                if "dominica" in line and "dominicanrepublic" in line and len(line.split("dominica")) > 2:
                    t.write("1")
                elif "dominica" in line and not "dominicanrepublic" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'GUINEA':
                if "guinea" in line and "equatorialguinea" in line and "guinea-bissau" in line and len(line.split("guinea")) > 3:
                    t.write("1")
                elif "guinea" in line and "equatorialguinea" in line and not "guinea-bissau" in line and len(line.split("guinea")) > 2:
                    t.write("1")
                elif "guinea" in line and not "equatorialguinea" in line and "guinea-bissau" in line and len(line.split("guinea")) > 2:
                    t.write("1")
                elif "guinea" in line and not "equatorialguinea" in line and not "guinea-bissau" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'IRAN':
                if "iran" in line and not "iran(islamicrepublicof)" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'NIGER':
                if "niger" in line and "nigeria" in line and len(line.split("niger")) > 2:
                    t.write("1")
                elif "niger" in line and not "nigeria" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'SUDAN':
                if "sudan" in line and "southsudan" in line and len(line.split("sudan")) > 2:
                    t.write("1")
                elif "sudan" in line and not "southsudan" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'MALI':
                if "mali" in line and "somalia" in line and len(line.split("mali")) > 2:
                    t.write("1")
                elif "mali" in line and not "somalia" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'OMAN':
                if "oman" in line and "romania" in line and len(line.split("oman")) > 2:
                    t.write("1")
                elif "oman" in line and not "romania" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'IRELAND':
                if "ireland" in line and "unitedkingdomofgreatbritainandnorthernireland" in line and len(line.split("ireland")) > 2:
                    t.write("1")
                elif "ireland" in line and not "unitedkingdomofgreatbritainandnorthernireland" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country == 'VENEZUELA (BOLIVARIAN REPUBLIC OF)':
                if "venezuela" in line:
                    t.write("1")
                else:
                    t.write("0")
            elif country.lower().replace(" ","") in line:
                t.write("1")
            else:
                t.write("0")
            t.write('\t')
        t.write('\n')
t.close()