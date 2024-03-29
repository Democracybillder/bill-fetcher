''' Pulls all Legiscan related information, both from their API and associated files '''

import requests
import csv
import logging


def request_session_list(state):
    ''' Returns Legiscan request for a state's session list '''
    return request_data('getSessionList', ('state',), (state,))

def request_state_bill_list(state):
    ''' Returns Legiscan request for a state's current session bill list '''
    return request_data('getMasterList', ('state',), (state,))

def request_session_bill_list(session_id):
    ''' Returns Legiscan request for a session's bill list '''
    return request_data('getMasterList', ('id',), (session_id,))

def aggregate_all_sessions():
    ''' Generates dict where keys = states and values = session id tuples from
    Legiscan'''
    state_sessions = {}
    for state in get_states():
        ids = compile_state_session_ids(request_data('getSessionList', ('state',), (state, )))
        state_sessions[state] = ids
    return state_sessions

def request_data(operation, param, value):
    ''' Takes method and key tuples and returns request
    object of bills for a given state from legiscan '''
    keys = {}
    count = 0
    assert len(param) == len(value), "Must have same number of params and values!"
    for name in param:
        keys[name] = value[count]
        count += 1
    params = {'key':'ff6da19238f87945db1c0dd5d6bc1674',
              'op' : operation}
    params.update(keys)
    req = requests.get('http://api.legiscan.com/?', params=params)
    data = req.json()
    logging_data(data)
    return data

def compile_state_session_ids(data):
    '''Takes state sessions request objects and converts to tuple'''
    sessions = []
    for instance in data["sessions"]:
        session_id = instance["session_id"]
        sessions.append(session_id)
    sessions = tuple(sessions)
    return sessions

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

def logging_data(data):
    ''' Checks if data is corrupt and raises warning to log file if needed '''
    if type(data) != dict or data["status"] != "OK" or len(data) != 2:
        logging.warning('Legiscan data type not dict (type = %s) \
         or data["status"] not "OK" (status = %s) \
         or len(data) not 2 (len(data) = %s)' \
        , type(data), data["status"], len(data))

