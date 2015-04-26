
''' pulls session years data from legiscan api and populates db'''

import csv
import requests # requests needs to be installed for this to work ($ git clone git://github.com/kennethreitz/requests.git)
import db

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
    '''Takes state string and returns JSON of sessions for state from legiscan'''
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op': 'getSessionList',
              'state':state}
    req = requests.get('http://api.legiscan.com/?', params=params)
    return req

def compileStateSessions(request):
    '''Takes state sessions request objects and edits it to db specifications'''
    original = request.json()
    sessions = []
    for instance in original["sessions"]:
    	session = {
    		"session_id":instance["session_id"],
    		"year_start":instance["year_start"],
    		"year_end":instance["year_end"],
    		"session":instance["session_name"]
    		}
    	sessions.append(session)
    sessions = tuple(sessions)
    database = db
    database.insertsessiondata('billder',sessions)

def getAllStateSessions():
	for state in getStates():
		compileStateSessions(pullStateData(state))

print getAllStateSessions()
