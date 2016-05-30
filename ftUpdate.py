import requests
import re
import HTMLParser
import time 

# Supress Unverified SSL Session Error
requests.packages.urllib3.disable_warnings()

#Go to Sourcefire Security Enhancement List
urlMainPage = 'https://support.sourcefire.com/notices/seus/'
resultMainPage=requests.get(urlMainPage, verify=False)
print "***Checking Updates from: " + urlMainPage
print "\n"

#Grep the latest update version
patternVer = re.compile('notices/seus/[0-9]{4}',re.IGNORECASE)
matchesMainPage =  patternVer.findall(resultMainPage.text)
strUpdatePage = ''.join(matchesMainPage)
verUpdate =  strUpdatePage[13:17]

resultMainPage.close()

#Go to Sourcefire Update page
urlUpdate = urlMainPage + verUpdate
resUpdate=requests.get(urlUpdate, verify=False)

#Grep Sourcefire Rules from Update page
patternSFRules = re.compile('sf-rules-[0-9]{4}-[0-9]{2}-[0-9]{2}')
matchSFRules = patternSFRules.findall(resUpdate.text)
strRulesPage = ''.join(matchSFRules)

#Go to Sourcefire Rules page
urlSFRules = "https://support.sourcefire.com/supplemental/" + strRulesPage + "-mod.html"
resSFRules = requests.get(urlSFRules,verify=False) 
print "***Pulling Sourcefire updates from: https://support.sourcefire.com/supplemental/" + strRulesPage + "-mod.html"
print "\n"

#Parse Sourcefire  Rules page table
data = resSFRules.text

class TableParser(HTMLParser.HTMLParser):
	def __init__(self):
            HTMLParser.HTMLParser.__init__(self)
            self.in_td = False
            self.data = []
     
        def handle_starttag(self, tag, attrs):
            if tag == 'td':
                self.in_td = True
       
        def handle_data(self, data):
            if self.in_td:
               self.data.append(data)
	       
        
        def handle_endtag(self, tag):
            self.in_td = False
 
parserRules = TableParser()
parserRules.feed(data)
string = ';'.join(parserRules.data)

#Dump Rules to text

fileDump = open('sfRulesDump','w+')
fileDump.write(string)
fileDump.close()
parserRules.close()

# Align Rules
fileIn = open('sfRulesDump','r+')
f00 = fileIn.read()
fileIn.close()


list = f00.split(';')
fileOut = open('sfRulesAligned','w+')

x=0

for item in list:
	if "DELETED" not in item:
        	fileOut.write("%s"%item)
        	x += 1
        	if (x == 7):
                	fileOut.write("\n")
                	x=0
		else:
			fileOut.write("\t")
	else:
		fileOut.write("%s"%item)
		fileOut.write("\t")
		x = 6

fileOut.close()

#Go to ET Update Summary page
urlETSummary = 'http://www.proofpoint.com/us/daily-ruleset-update-summary'
resETPage = requests.get(urlETSummary)
print "***Checking Updates from: " + urlETSummary
print "\n"

#Grep to latest update page
patETupdate = re.compile('(:?[0-9]{4}\-[0-9]{2}\-[0-9]{2})')
matchETRules = patETupdate.findall(resETPage.text)
strETRulesPage = ''.join(matchETRules)
strETRulesPage =  strETRulesPage[:10]
print "Regex match: " + strETRulesPage

#Go to ET Rules page
urlETRules = "http://www.proofpoint.com/us/daily-ruleset-update-summary-" + strETRulesPage
resETRules = requests.get(urlETRules)

print "***Pulling ET updates from: " + urlETRules
print "\n"

#Dump ET Rules to file
etDump = open('etRulesDump','w+')
etDump.write(resETRules.text.encode("utf-8"))
etDump.close()

#Parse ET Rules
filebuf = open("etRulesDump","rb").read()

patternActive = re.compile('(?<=Added\srules:)(.*)(?=\[\/\/\/])',re.DOTALL)
patternRules = re.compile ('[0-9]{7}\s-\sET.*?\)')

#Grab only Active rules
lstActiveRules = patternActive.findall(filebuf,re.DOTALL)
#print filebuf

lstRules = []
#Grab individual rules
for rules in lstActiveRules:
	lstRules = patternRules.findall(rules)

#Dump aligned rules
etFileOut = open('etRulesAligned','w')

for rule in lstRules:
	etFileOut.write("%s\n"%rule)
etFileOut.close()

#Start Crawling
execfile('ftCrawl.py')

