#!/usr/bin/python
''' pulls bill data from the legiscan api and populates the db. 
get_all_state_bills() initiates db, get_all_state_bills updates existing db
WARNING: Do not run the code close to midnight, the date changes will have
adverse effects '''
import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import db
import datetime
import threading # for auto updating

# To run automatically updating db

def update_db_every_seconds(interval, number):
    '''updates db every number of seconds (float) inputted a specified number 
    of times (int)'''
    if number <= 0:
        print "Finished updating DB the specified number of times. (good job me)"
    else:
        get_all_state_bills()
        threading.Timer(interval, update_db_every_seconds, [interval, number-1]).start()

# Wrapper methods for updating and initializing db

def get_all_state_bills():
    ''' Gets all full edited bill info from all states from LegiScan into db'''
    state_sessions = aggregate_all_sessions()
    for state in state_sessions:
        for session in state_sessions[state]:   # Because dict with tuple values
            object_to_db(request_data(session, 'getMasterList'), state, 0)
    db.updatelastdbmodification('billder') # update db update log

def get_updated_state_bills():
    ''' Gets updated bill info for all states from Legiscan into db'''
    updated = db.getlastdbmodification('billder')
    for state in get_states():
        object_to_db(request_data(state, 'getMasterList'), state, updated[0][0])
    db.updatelastdbmodification('billder')    # update db update log

def object_to_db(request, state, updated):
    ''' Wrapper function that organizes use of update and non-update functions'''
    master_list, session = clean_request(request)
    if updated == 0:
        return insert_bills_into_db(all_state_bills(master_list, session, state))
    elif isinstance(updated, datetime.datetime):
        return insert_bills_into_db(updated_state_bills(master_list, session, state, updated))
    else: print "argument must be either db last modification date for updating db or '0' for initializing db"

# Inserting tuples into db

def insert_bills_into_db(data):
    bills_desc, bills_log = data
    db.insertbills('billder', bills_desc, bills_log)

# Parsing through objects to distill tuples

def all_state_bills(master_list, session, state):
    ''' Takes full state bills list, session id and state and returns two tuples objects '''
    bills_desc = []
    bills_log = []
    for bill in master_list:
            bill = clean_invalid_dates(bill)
            bill_desc = distill_bill_desc(bill, state, session)
            bills_desc.append(bill_desc)
            bill_log = distill_bill_log(bill)
            bills_log.append(bill_log)
    bills_desc, bills_log = tuple(bills_desc), tuple(bills_log)
    return bills_desc, bills_log

def updated_state_bills(master_list, session, state, updated):
    ''' Takes full bill tuples, state name, session id and db last update and returns 
    updated bills only in two tuples '''
    bills_desc = []
    bills_log = []
    for bill in master_list:
        bill = clean_invalid_dates(bill)
        bill_date = is_real_date(bill["last_action_date"], 1)
        if bill_date == None or bill_date > updated:
            bill_log = distill_bill_log(bill)
            bills_log.append(bill_log)
            status = bill["status"]
            status_date = is_real_date(bill["status_date"], 1)
            if status_date == bill_date and int(status) == 1: # new bill
                bill_desc = distill_bill_desc(bill, state, session)
                bills_desc.append(bill_desc)
    bills_desc = tuple(bills_desc)
    bills_log = tuple(bills_log)
    return bills_desc, bills_log

def distill_bill_log(bill):
    '''takes bill and returns billLog Tuple'''
    bill_log = {
                "bill_id": bill["bill_id"],
                "status_date": bill["status_date"],
                "status": bill["status"],
                "last_action_date": bill["last_action_date"],
                "last_action": bill["last_action"]
                }
    return bill_log

def distill_bill_desc(bill, state, session):
    '''takes bill and returns billDesc Tuple'''
    bill_desc = {
                "state": state,
                "bill_id":bill["bill_id"],
                "session_id": session,
                "number": bill["number"],
                "title": bill["title"],
                "description": bill["description"]
                }
    return bill_desc

# Legiscan APIs/ reference files:

def get_states():
    ''' Returns list of LegiScan Abbreviated State names from LegiScan source 
    csv '''
    states = []
    with open('reference-files/state.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            states.append(row[1])
    states = states[1:53]
    return states

def request_data(value, operation):
    ''' Takes string for state or int for session id and returns request object 
    of bills for a given state from legiscan '''
    if isinstance(value, str):
        param = 'state'
    elif isinstance(value, int):
        param = 'id'
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op': operation,
              param : value}
    req = requests.get('http://api.legiscan.com/?', params=params)
    return req

# Helper functions to clean request objects

def clean_request(request):
    ''' Parses session data and bill data from request object '''
    original = request.json()
    session = original["masterlist"]["session"]["session_id"]
    del original["masterlist"]["session"]
    master_list = original["masterlist"].values() # turns dict into list of bills (gets rid of useless number keys)
    return master_list, session

def compile_state_session_ids(request):
    '''Takes state sessions request objects and converts to tuple'''
    original = request.json()
    sessions = []
    for instance in original["sessions"]:
        session_id = instance["session_id"]
        sessions.append(session_id)
    sessions = tuple(sessions)
    return sessions

def aggregate_all_sessions():
    '''generates dict of states for keys and session id tuples for values from 
    Legiscan'''
    state_sessions = {}
    for state in get_states():
        ids = compile_state_session_ids(request_data(state, 'getSessionList'))
        state_sessions[state] = ids
    return state_sessions

# Functions to facilitate date comparisons

def clean_invalid_dates(bill):
    ''' Makes sure bill is either None or datetime object if needed '''
    bill["status_date"] = is_real_date(bill["status_date"])
    bill["last_action_date"] = is_real_date(bill["last_action_date"])
    return bill

def is_real_date(date_text, compare=0):
    ''' Checks if date given is real or corrupt, convert string to datetime if needed'''
    try:
        date = datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
        if compare == 1:
            return date
        else:
            return date_text
    except ValueError:
        return None

get_all_state_bills()


