#!/usr/bin/python
''' pulls bill data from the legiscan api and populates the db. 
getAllStateBills() initiates db, getUpdatedStateBills updates existing db '''
import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import db
import datetime
import threading # for auto updating

# To run automatically updating db

def updateDBEverySeconds(interval,number):
    '''updates db every number of seconds (float) inputted a specified number 
    of times (int)'''
    if number <= 0:
        print "Finished updating DB the specified number of times. (good job me)"
    else:
        getUpdatedStateBills()
        threading.Timer(interval,updateDBEverySeconds,[interval,number-1]).start()

# Wrapper methods for updating and initializing db

def getAllStateBills():
    ''' Gets all full edited bill info from all states from LegiScan into db'''
    stateSessions = aggregateAllSessions()
    for state in stateSessions:
        for session in stateSessions[state]:   # Because dict with tuple values
            objectToDB(requestData(session,'getMasterList'),state,0)
    updatelastdbmodification('billder') # update db update log

def getUpdatedStateBills():
    ''' Gets updated bill info for all states from Legiscan into db'''
    updated = db.getlastdbmodification('billder')
    for state in getStates():
        objectToDB(requestData(state,'getMasterList'),state,updated[0][0])
    updatelastdbmodification('billder')    # update db update log

def objectToDB(request, state, updated):
    ''' Wrapper function that organizes use of update and non-update functions'''
    masterList, session = cleanRequest(request)
    if updated == 0:
        return insertBillsIntoDB(allStateBills(masterList,session,state))
    elif type(updated) == datetime.datetime:
        return insertBillsIntoDB(updatedStateBills(masterList,session,state,updated))
    else: print "argument must be either db last modification date for updating db or '0' for initializing db"

# Inserting tuples into db

def insertBillsIntoDB(data):
    billsDesc, billsLog = data
    database = db
    database.insertbills('billder', billsDesc, billsLog)

# Parsing through objects to distill tuples

def allStateBills(masterList,session,state):
    ''' Takes full state bills list and returns two tuples objects '''
    billsDesc = []
    billsLog = []
    for bill in masterList:
            bill = cleanInvalidDates(bill)
            billDesc = {
                "state": state,
                "bill_id":bill["bill_id"],
                "session_id": session,
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
    billsDesc, billsLog = tuple(billsDesc), tuple(billsLog)
    return billsDesc, billsLog

def updatedStateBills (masterList,session,state,updated):
    ''' Takes full bill tuples and state name and returns updated bills only 
    in two tuples '''
    billsDesc =[]
    billsLog = []
    count_new_bills = 0
    count_updates = 0
    for bill in masterList:
        bill = cleanInvalidDates(bill)
        billDate = isDateNone(bill["last_action_date"])
        if billDate < updated: # don't need old data
            continue
        else:
            count_updates += 1
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
                count_new_bills +=1
                billDesc = {
                    "state": state,
                    "bill_id":bill["bill_id"],
                    "session_id": session,
                    "number": bill["number"],
                    "title": bill["title"],
                    "description": bill["description"]
                    }
                billsDesc.append(billDesc)
    print 'count_new_bills =', count_new_bills, 'count_updates =', count_updates
    billsDesc = tuple(billsDesc)
    billsLog = tuple(billsLog)
    return billsDesc, billsLog

# Legiscan APIs/ reference files:

def getStates():
    ''' Returns list of LegiScan Abbreviated State names from LegiScan source 
    csv '''
    states = []
    with open('reference-files/state.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            states.append(row[1])
    states = states[1:53]
    return states

def requestData(value,op):
    ''' Takes string for state or int for session id and returns request object 
    of bills for a given state from legiscan '''
    if type(value) == str:
        param = 'state'
    elif type(value) == int:
        param = 'id'
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op': op,
              param : value}
    req = requests.get('http://api.legiscan.com/?', params=params)
    return req

# Helper functions to clean request objects

def cleanRequest(request):
    ''' Parses session data and bill data from request object '''
    original = request.json()
    session = original["masterlist"]["session"]["session_id"]
    del original["masterlist"]["session"]
    masterList = original["masterlist"].values() # turns dict into list of bills (gets rid of useless number keys)
    return masterList, session

def compileStateSessionIDs(request):
    '''Takes state sessions request objects and converts to tuple'''
    original = request.json()
    sessions = []
    for instance in original["sessions"]:
        session_id = instance["session_id"]
        sessions.append(session_id)
    sessions = tuple(sessions)
    return sessions

def aggregateAllSessions():
    '''generates dict of states for keys and session id tuples for values from 
    Legiscan'''
    stateSessions = {}
    for state in getStates():
        ids = compileStateSessionIDs(requestData(state,'getSessionList'))
        stateSessions[state] = ids
    return stateSessions

# Functions to facilitate date comparisons

def cleanInvalidDates(bill):
    ''' Checks if dates in bill are real '''
    valstatdate = isRealDate(bill["status_date"])
    if valstatdate == 0:
        bill["status_date"] = None
    valactiondate = isRealDate(bill["last_action_date"])
    if valactiondate == 0:
        bill["last_action_date"] = None
    return bill

def isDateNone(date):
    '''Replaces "None" dates with today to be updated after date comparisons'''
    try:
        billDate = datetime.datetime.strptime(date,'%Y-%m-%d')
        return billDate
    except TypeError:
        print datetime.datetime.now() #So appears to be updated, just in case
        assert False

def isRealDate(date_text):
    ''' Checks if date given is real or corrupt data '''
    try:
        datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
        return 1
    except ValueError:
        return 0


getUpdatedStateBills()
#getAllStateBills()

