#!/usr/bin/python
''' pulls bill data from the legiscan api and populates the db '''
''' To work offline: 1) import ast 2) replace requestData(state) with " with open('req.txt', 'r') as output: #for offline testing 
        req = output.read()", 3) in clearRequest, replace "request.json()" with ast.literal_eval(request) 
'''
import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import db
import datetime


def getStates():
    ''' Returns list of LegiScan Abbreviated State names from LegiScan source csv '''
    states = []
    with open('reference-files/state.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            states.append(row[1])
    states = states[1:53]
    return states

def requestData(state):
    ''' Takes state string and returns JSON of bills for state from legiscan '''
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op':'getMasterList',
              'state':state}
    req = requests.get('http://api.legiscan.com/?', params=params)
    return req

def cleanRequest(request):
    ''' Takes state bills request objects and edits it to db specifications '''
    #print 'in cleanRequest'
    original = request.json()
    session = original["masterlist"]["session"]["session_name"]
    del original["masterlist"]["session"]
    masterList = original["masterlist"].values() # turns dict into list of bills (gets rid of useless number keys)
    return masterList, session

def cleanInvalidDates(bill):
    ''' Checks if dates in bill are real '''
    #print 'in cleanInvalidDates'
    valstatdate = isRealDate(bill["status_date"])
    if valstatdate == 0:
        bill["status_date"] = None
    valactiondate = isRealDate(bill["last_action_date"])
    if valactiondate == 0:
        bill["last_action_date"] = None
    return bill

def isDateNone(date):
    '''deals with None dates for date comparisons'''
    try:
        billDate = datetime.datetime.strptime(date,'%Y-%m-%d')
        return billDate
    except TypeError:
        return datetime.datetime.now() #So appears to be updated, just in case

def isRealDate(date_text):
    ''' Checks if date given is real or corrupt data '''
    #print 'in isRealDate'
    try:
        datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
        return 1
    except ValueError:
        return 0

def objectToTuples(request, state, updated=1):
    ''' Takes state bills request object and returns two tuples objects '''
    #print 'in objectToTuples'
    masterList, session = cleanRequest(request)
    if updated == 1:
        return updatedStateBills(masterList,session,state)
    else:
        return allStateBills(masterList,session,state)
        
def allStateBills(masterList,session,state):
    ''' Takes full state bills list and returns two tuples objects '''
    billsDesc = []
    billsLog = []
    for bill in masterList:
            bill = cleanInvalidDates(bill)
            billDesc = {
                "state": state,
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
    return billsDesc, billsLog

def updatedStateBills (masterList,session,state):
    ''' Takes updated state bills list and returns two tuples objects '''
    #print 'in updatedStateBills'
    billsDesc =[]
    billsLog = []
    lastDBDate = DBDate()
    for bill in masterList:
        bill = cleanInvalidDates(bill)
        billDate = isDateNone(bill["last_action_date"])
        if billDate < lastDBDate: # don't need old data
            continue
        else:
            billLog = {
                "bill_id": bill["bill_id"],
                "status_date": bill["status_date"],
                "status": bill["status"],
                "last_action_date": bill["last_action_date"],
                "last_action": bill["last_action"]
                }
            billsLog.append(billLog)
            statusDate = isDateNone(bill["status_date"])
            if statusDate == billDate: # new bill
                billDesc = {
                    "state": state,
                    "bill_id":bill["bill_id"],
                    "session": session,
                    "number": bill["number"],
                    "title": bill["title"],
                    "description": bill["description"]
                    }
                billsDesc.append(billDesc)
    billsDesc = tuple(billsDesc)
    billsLog = tuple(billsLog)

def DBDate():
    ''' Gets most recent date from DB for last added data. For now, date for testing '''
    return datetime.datetime.strptime("2015-04-21", '%Y-%m-%d')

def insertIntoDB(billsDesc, billsLog):
    database = db
    database.insertbills('billder', billsDesc, billsLog)

def getAllStateBills():
    ''' Gets full edited bill info of all states from LegiScan '''
    for state in getStates():
        objectToTuples(requestData(state),state,0)

def getUpdatedStateBills():
    ''' Gets updated bill info for all states from Legiscan '''
    for state in getStates():
        objectToTuples(requestData(state),state)

#objectToTuples(requestData('NY'),'NY')
#getUpdatedStateBills()
#getAllStateBills()
#insertIntoDB(objectToTuples(requestData("IN","getMasterList"),"IN"))
# NY bill 773487 status = 1 and statusdate = lastaction date (04/22)
