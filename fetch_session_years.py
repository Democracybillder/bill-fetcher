
''' pulls session years data from legiscan api and populates db'''
import db
import billdb
import legiscan
import json # for configuration file parsing


##################################################
## Get database connection details from json config file
## SHould be moved into the main file once there is one and the program is  neater


def dbinit():
    """ initializing db connection """
    with open('config.json') as json_conf_file:
        conf = json.load(json_conf_file)
    database = db.DB(conf["postgres"])

    return billdb.BillDB(database)


BILLDB = dbinit()
####################################################

def get_all_state_sessions():
    ''' Wrapper method for getting all session info '''
    tups = []
    for state in legiscan.get_states():
        data = legiscan.request_data('getSessionList', ('state',), (state,))
        tups += compile_state_sessions(data)
    BILLDB.insert_session_data(tuple(tups))

def compile_state_sessions(data):
    '''Takes state sessions data and parses info '''
    sessions = []
    for instance in data["sessions"]:
        session = {
            "session_id":instance["session_id"],
            "year_start":instance["year_start"],
            "year_end":instance["year_end"],
            "session":instance["session_name"]
            }
        sessions.append(session)
    return sessions
