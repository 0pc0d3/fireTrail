import re

print "+++++++++++++"
print "Crawling..."
print "+++++++++++++\n\n"

#Load Dumped Rules
rulesbuf = open("sfRulesAligned","rb").read()
sfRules = rulesbuf.splitlines()

#Load ET Dumped ET Rules
etrulesbuf = open("etRulesAligned","rb").read()
etRules = etrulesbuf.splitlines()

#Load Hot List
listbuf = open("hotList","rb").read()
list = listbuf.splitlines()

#Load History
historybuf = open("History","ra").read()
lstHistory = historybuf.splitlines()

#SID Pattern to add to History
patternSID = re.compile('[0-9]{5,10}\s')


fileHistory = open("History","a")
sfNotify = open("sfNotify","w")
etNotify = open("etNotify","w")

lstSFMatch = []	#List to hold all matched SF Rules
lstETMatch = []	#List to hold all matched ET Rules
lstSID = []	#List to hold matched SID

sfmatch = False
#Crawl SF Rules
for rule in sfRules:
	found = False	#Initialize found flag to False
	sid = ''.join(patternSID.findall(rule))
	sid = sid.strip()	#grab SID of rule
	for item in lstHistory:	#check if SID exist in History
		if sid == item:	#if SID matches an element in History
			found = True		#if found, set found flag to true
	if found != True:				#if rule SID not found in History
		for word in list:		#for each keyword 
			if word.lower() in rule.lower():	#if keyword found in rule
				lstSID.append(sid)
				lstSFMatch.append(word+'\t'+rule)
				sfmatch = True
				break
etmatch = False
#Crawl ET Rules
for etRule in etRules:
	etfound = False	#Initialize found flag to False
        etsid = ''.join(patternSID.findall(etRule))
        etsid = etsid.strip()       #grab SID of rule
        for item in lstHistory: #check if SID exist in History
		if etsid == item: #if SID matches an element in History
                        etfound = True            #if found, set found flag to tr$        	
	if etfound != True:
	       	for word in list:
               		if word.lower() in etRule.lower():      #if keyword found in rule
                       		lstSID.append(etsid)
                      		lstETMatch.append('[Keyword: '+word+']\t'+etRule)
                       		etmatch = True
				break


#Add rule SID to History
for item in lstSID:
	fileHistory.writelines(item+'\n')

#Add rule to SF Notification
for item in lstSFMatch:
	sfNotify.writelines(item+'\n')

#Add rule to ET Notification
for item in lstETMatch:
	etNotify.writelines(item+'\n')


fileHistory.close()
sfNotify.close()
etNotify.close()

if sfmatch or etmatch:
	execfile('ftNotify.py')
else:
	print "No new matches found...\nEither the latest rules did not have a match or matching rule was previously reported"
