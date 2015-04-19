#!/usr/bin/python
''' pulls bill data from the legiscan api and populates the db'''
# TODO:
# - save only one instance for bills with more than one action
# - Decouple editStateBills

import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import db
import datetime

def isRealDate(date_text):
    ''' validates dates '''
    try:
        datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
        return 1
    except ValueError:
        return 0

def getStates():
    '''Returns list of LegiScan Abbreviated State names from LegiScan source csv'''
    states = []
    with open('reference-files/state.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            states.append(row[1])
    states = states[1:53]
    return states


def pullStateData(state):
    '''Takes state string and returns JSON of bills for state from legiscan'''
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op': 'getMasterList',
              'state':state}
    req = requests.get('http://api.legiscan.com/?', params=params)
    return req

def compileStateBills(request, state):
    '''Takes state bills request object and returns two tuples objects'''
    billsDesc = []
    billsLog = []
    masterList, session = editStateBills(request)
    for bill in masterList:
        print 'pre-bill = ', bill
        bill = validateDate(bill)
        print 'post-bill =,', bill
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

    database = db
    database.insertbills('billder', billsDesc, billsLog)

def editStateBills(request):
    '''Takes state bills request objects and edits it to db specifications'''
    original = request.json()
    session = {}
    session['session_name'] = original["masterlist"]["session"]["session_name"]
    # session["year_start"] = original["masterlist"]["session"]["year_start"]
    # session["year_end"] = original["masterlist"]["session"]["year_end"]
    del original["masterlist"]["session"]
    masterList = original["masterlist"].values() # turns dict into list of bills (gets rid of useless number keys)
    return masterList, session

def validateDate(bill):
    valstatdate = isRealDate(bill["status_date"])
    if valstatdate == 0:
        bill["status_date"] = None
    valactiondate = isRealDate(bill["last_action_date"])
    if valactiondate == 0:
        bill["last_action_date"] = None
    return bill

def getAllStateBills():
    '''Gets full edited bill history of all states from LegiScan'''
    for state in getStates():
        compileStateBills(pullStateData(state),state)

#getAllStateBills()
compileStateBills(pullStateData("IN"),"IN")

