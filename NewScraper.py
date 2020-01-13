import re
import dateutil.parser as parser
import linkGrabber
import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd
from datetime import date, timedelta
import httplib2

#DECLARING .CSV OUTPUT FILE
CSV_FILE = r"OrbitalLaunchesOutput.csv"

#YOU CAN MODIFY THE YEAR
#for i in range(1972,2019):
YEAR = "2019"
#print(YEAR)

#URL TO SERACH
URL = 'https://en.wikipedia.org/wiki/'+YEAR+'_in_spaceflight#Orbital_launches'

#GET REQUEST (HTML FORMAT)
RESPONSE = requests.get(URL, allow_redirects=True)

CONTENT_OF_PAGE = RESPONSE.content
#print(CONTENT_OF_PAGE)
#FILE1 = open("page.html", "w")
#FILE1.write(str(CONTENT_OF_PAGE))
#FILE2 = open("page.html", "r")
#CONTENT_HTML = FILE2.read()
#FILE1.close()

#SOUP = BeautifulSoup(str(CONTENT_HTML), features="lxml")
SOUP = BeautifulSoup(str(CONTENT_OF_PAGE), features="lxml")
#FILE2.close()

#print('***************************************************************************************************************************')

TABLE = SOUP.find('table', {'class':'wikitable collapsible'} )
#print(table)
ROWS=list()
COUNTER=0

DatesDict=dict()

START_DATE_OF_YEAR = date(int(YEAR), 1, 1)   # start date
END_DATE_OF_YEAR = date(int(YEAR), 12, 31)   # end date

DATE_DAYS = END_DATE_OF_YEAR - START_DATE_OF_YEAR       # as timedelta
COUNT_DAYS=0
for i in range(DATE_DAYS.days + 1):
    DAY = START_DATE_OF_YEAR + timedelta(days=i)
    COUNT_DAYS+=1
    DATE = parser.parse(str(DAY))
    ISO_DATE = DATE.isoformat()
    DatesDict[str(ISO_DATE)+"+00:00"]=0
print(COUNT_DAYS)

START_OF_LAUNCH_FLAG=0
NewTag=""

for ROW in TABLE.findAll("tr"):
    #i = soup.select("span.nowrap")
    #print('__________________________________________________________________________________________________________________________')
    #print(ROW)

    if (str(ROW)[28:42] == 'class="nowrap"' or str(ROW)[29:43] == 'class="nowrap"'):
        START_OF_LAUNCH_FLAG=1
        #print('__________________________________________________________________________________________________________________________')
        #print(ROW)
        left = 'class="nowrap">'
        right = 0
        # Output: 'string'
        s=str(ROW)
        le=s.index(left) + len(left)
        ri=s.index(left) + 30
        Tag=(str(ROW)[le:ri])
        NewTag=re.sub('<(.*)','',Tag) + ', '+ YEAR
        #print(NewTag)

    else:
        if START_OF_LAUNCH_FLAG == 1:
            STATUS = str(ROW)[-200:]
            if 'Successful' in STATUS or 'Operational'in STATUS or 'En route' in STATUS or 'Success' in STATUS:
                START_OF_LAUNCH_FLAG = 0
                #print(NewTag)
                try:
                    DATE = parser.parse(NewTag)
                    ISO_DATE = DATE.isoformat()
                    #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    #print(ISO_DATE)
                    if str(ISO_DATE)+"+00:00" in DatesDict:
                        DatesDict[str(ISO_DATE)+"+00:00"] += 1
                        COUNTER+=1
                except:
                    print("~~~~~~~ KEY ERROR ~~~~~~~")


#print(DatesDict)

DataFrame=pd.DataFrame(list(DatesDict.items()), columns=['date', 'value'])
print(DataFrame)
print(COUNTER)
DataFrame.to_csv(CSV_FILE,index=False)
