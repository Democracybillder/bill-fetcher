import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import json

def getStates():
    # Returns list of LegiScan Abbreviated State names from LegiScan source csv
    states = []
    with open('reference-files/state.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        for row in reader:
            states.append(row[1])
    states = states[1:52]
    return states


def pullStateData(state):
    # Takes state string and returns JSON of bills for state from legiscan
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op': 'getMasterList',
              'state':state}
    r = requests.get('http://api.legiscan.com/?',params=params)
    return r


def editStateBills(request):
    # Takes state bills request object and edits it to DB specifications, returns two tuples objects)
    billsDesc = []
    billsLog = []
    original = request.json()
    session = original["masterlist"]["session"]["session_name"]
    del original["masterlist"]["session"]
    masterList = original["masterlist"].values() # turns dict into list of bills (gets rid of useless number keys)
    for bill in masterList:
        billDesc = {
            "bill_id":bill["bill_id"],
            "session": session,
            "number": bill["number"],
            "title": bill["title"],
            "description": bill["description"]
            }
        billLog = {
            "bill_id": bill["bill_id"],
            "status_date": bill["status_date"],
            "status": bill["status"],
            "last_action_date": bill["last_action_date"],
            "last_action": bill["last_action"]
        }
        billsDesc.append(billDesc)
        billsLog.append(billLog)
    billsDesc = tuple(billsDesc)
    billsLog = tuple(billsLog)
    #Insert method to insert data to database

def getAllStateBills():
    # Gets full edited bill history of all states from LegiScan
    for state in getStates():
        editStateBills(pullStateData(state))