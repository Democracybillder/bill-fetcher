#!/usr/bin/python
''' get_all_state_bills() initiates db, get_updated_state_bills() updates existing db
WARNING: Do not run the code close to midnight, the date changes will have
adverse effects '''
import bills
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

# Wrapper methods for updating and initializing db


def get_all_state_bills():
    ''' Gets all full bill info from all states from LegiScan into db'''
    state_sessions = legiscan.aggregate_all_sessions()
    for state in state_sessions:
        for session in state_sessions[state]:   # Because dict with tuples
            session_bills = bills \
            .StateBillsObject(legiscan.request_session_bill_list(session), state)
            session_bills.all_state_bills()
            BILLDB.insert_bills(session_bills.desc, session_bills.log)
    BILLDB.update_last_db_modification()    # update db update log

def get_updated_state_bills():
    ''' Gets updated bill info only for all states from Legiscan into db, based on db last
    update log '''
    updated = BILLDB.get_last_db_modification()
    for state in legiscan.get_states():
        state_bills = bills.StateBillsObject(legiscan.request_state_bill_list(state), state)
        state_bills.updated_state_bills(updated[0][0], BILLDB)
        BILLDB.insert_bills(state_bills.desc, state_bills.log)
    BILLDB.update_last_db_modification()    # update db update log


get_all_state_bills()


