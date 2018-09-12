import csv
import math
import xml.etree.ElementTree as ET
import urllib
import zipfile
import cStringIO
import requests

moveon = raw_input('ICAO?')
jobnum = input('Min number of pax?')
PT = ""
latlong = dict()
distance = dict()
try:
    with open('AccessKey.txt') as myfile:
        userkey = myfile.read()
except:
    userkey = raw_input("What is your Datafeeds AccessKey?")
    textfile = open("AccessKey.txt", "w+")                  
    textfile.write(userkey)                                 
    textfile.close()                                        

def homepage(icao):
    datafeed = 'http://server.fseconomy.net/data?userkey=' + userkey + '&format=xml&query=icao&search=jobsfrom&icaos=' + icao
    urllib.urlretrieve(datafeed, "file.xml")
    tree = ET.parse('file.xml')
    root = tree.getroot()
    return root

def airportdata():
    r = requests.get('http://server.fseconomy.net/static/library/datafeed_icaodata.zip')
    z = zipfile.ZipFile(cStringIO.StringIO(r.content))
    z.extractall()
    return()

def airportcsv():
    with open('icaodata.csv') as icaodata:
        csvreader = csv.reader(icaodata, delimiter= ',')
        for row in csvreader:
            if row[0] in goodjobset2:

                latlo = row[1], row[2]
                latlong.update({row[0]:latlo})
    return latlong

def distancecalc(lat1,lat2,long1,long2):
    lat2 = math.radians(lat2)
    lat1 = math.radians(lat1)
    long2 = math.radians(long2)
    long1 = math.radians(long1)
    a = (math.sin((lat2-lat1)/2)**2) + (math.cos(lat1) * math.cos(lat2) * (math.sin((long2-long1)/2)**2))
    c = 2 * (math.atan2(math.sqrt(a), math.sqrt(1-a)))
    d = 6371 * c
    d = d * .539957
    return d

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 -1)
    result[0::2] = lst
    return result

print "connecting"
root = homepage(moveon)
apintrest = {}
intrest1 = []
goodjobset = {}
goodjobset2 = []
icaocurrent = ''

for child in root:
    for assignment in child:
        if assignment.tag == '{http://server.fseconomy.net}ToIcao':
            icaocurrent = assignment.text
        if assignment.tag == '{http://server.fseconomy.net}PtAssignment' and assignment.text == 'true':
            if icaocurrent in apintrest:
                apintrest.update({icaocurrent: apintrest[icaocurrent] + amount})
            else:
                apintrest.update({icaocurrent: amount})
        if assignment.tag == '{http://server.fseconomy.net}Amount':
            amount = int(assignment.text)
for x in apintrest:
    if apintrest[x] >= jobnum and x not in intrest1:
        intrest1.append(x)

intrest2 = intersperse(intrest1, '-')
intrest2 = str(intrest2).translate(None, "',[] ")
root = homepage(intrest2)

for ap in intrest1:

    for child in root:
        for assignment in child:
            if assignment.tag == '{http://server.fseconomy.net}Location':
                icaocurrent = assignment.text

            if assignment.tag == '{http://server.fseconomy.net}PtAssignment' and assignment.text  == 'true':
                PT = 'true'
            if assignment.tag == '{http://server.fseconomy.net}ToIcao' and assignment.text == moveon.upper() and icaocurrent == ap and PT == 'true':
                if icaocurrent in goodjobset:
                    goodjobset.update({icaocurrent:goodjobset[icaocurrent] + amount})
                else:
                    goodjobset.update({icaocurrent:amount})
            if assignment.tag == '{http://server.fseconomy.net}Amount':
                amount = int(assignment.text)


for x in goodjobset:
    if goodjobset[x] >= jobnum and x not in goodjobset2:
        goodjobset2.append(x)

if root.tag == 'Error' and root.text == 'Invalid user key!':
    print 'There was an error. Please double check you Access Key. You can find it in AccessKey.txt'
elif root.tag == "Error":
    print root.text
elif len(goodjobset2) == 0:
    print "There are no jobs matching your criteria"
else:
    print goodjobset2
try:
    latlong = airportcsv()
except:
    airportdata()
    latlong = airportcsv()

if len(latlong) > 1:
    for ap in latlong:
        lat1 = float(latlong[ap][0])
        long1 = float(latlong[ap][1])
        for ap1 in latlong:
            lat2 = float(latlong[ap1][0])
            long2 = float(latlong[ap1][1])
            d = distancecalc(lat1,lat2,long1,long2)
            aps = ap,ap1
            if d != 0:
                distance.update({aps:d})

    distance1 = {}
    for key, value in distance.items():
        if value not in distance1.values():
            distance1[key] = value

    distance = sorted(distance1.iteritems(), key=lambda (k, v): (v, k), )
    print "('ICAO', 'ICAO') Nautical Miles"
    for x in distance:
        print x[0], int(x[1])

Exit = raw_input("Press any key to exit")
exit()
