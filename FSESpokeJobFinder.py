
#Version 1
import xml.etree.ElementTree as ET
import urllib
import time

moveon = raw_input('ICAO?')
jobnum = input('Min number of jobs?')
PT = ""
try:
    with open('AccessKey.txt') as myfile:
        userkey = myfile.read()
except:
    userkey = raw_input("What is your Datafeeds AccessKey?")
    textfile = open("AccessKey.txt", "w+")                  
    textfile.write(userkey)                                 
    textfile.close()                                        







def homepage(icao):
    print 'working'
    datafeed = 'http://server.fseconomy.net/data?userkey=' + userkey + '&format=xml&query=icao&search=jobsfrom&icaos=' + icao
    urllib.urlretrieve(datafeed, "file.xml")
    tree = ET.parse('file.xml')
    root = tree.getroot()
    
    return (root)
print "connecting"
time.sleep(10)
root = homepage(moveon)
#if moveon != '':
   # icao = moveon
   # homepage()


apintrest = []
intrest1 = []
goodjobset = []
goodjobset2 = []
icaocurrent = ''



for child in root:

    for assignment in child:

        if assignment.tag == '{http://server.fseconomy.net}ToIcao':
            icaocurrent = assignment.text
        if assignment.tag == '{http://server.fseconomy.net}PtAssignment' and assignment.text == 'true':
            apintrest.append(icaocurrent)



for x in apintrest:
    if apintrest.count(x) >= jobnum and x not in intrest1:
        intrest1.append(x)


for ap in intrest1:
    time.sleep(10)


    root = homepage(ap)
    for child in root:
        for assignment in child:

            if assignment.tag == '{http://server.fseconomy.net}Location':
                icaocurrent = assignment.text

            if assignment.tag == '{http://server.fseconomy.net}PtAssignment' and assignment.text  == 'true':
                PT = 'true'
            if assignment.tag == '{http://server.fseconomy.net}ToIcao' and assignment.text == moveon.upper() and PT == 'true':


                goodjobset.append(icaocurrent)


for x in goodjobset:
    if goodjobset.count(x) >= jobnum and x not in goodjobset2:
        goodjobset2.append(x)
if root.tag == 'Error' and root.text == 'Invalid user key!':
    print 'There was an error. Please double check you Access Key. You can find it in AccessKey.txt'
elif root.tag == "Error":
    print root.text
elif len(goodjobset2) == 0:
    print "There are no jobs matching your criteria"

else:
    print goodjobset2
    
Exit = raw_input("Press any key to exit")
exit()
