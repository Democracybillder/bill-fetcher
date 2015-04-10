import csv
from urllib2 import Request, urlopen, URLError



def getStates():
    # Returns list of LegiScan Abbreviated State names from LegiScan source csv
    states = []
    with open('reference-files/state.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        for row in reader:
            states.append(row[1])
    states = states[1:51]
    return states



url = 'http://api.legiscan.com/?key=ff6da19238f87945db1c0dd5d6bc1674&op=getMasterList&state=FL'
request = Request(url)
try:
    response = urlopen(request)
    bills = response.read()
    print bills[:80]
except URLError, e:
    print 'No bills. Got an error code:', e
