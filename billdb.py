#!/usr/bin/python
'''db layer for bills'''

class BillDB(object):
    """ database logic for bills """
    _db = None

    def __init__(self, db):
        """ get db object to access """
        self._db = db

    def get_last_db_modification(self):
        """ fetching the last timestamp of data modification from the db"""
        query = """ SELECT MAX(last_updated) FROM update_log """
        return self._db.select(query, '')

    def update_last_db_modification(self):
        """ updating the last timestamp of data modification in the db"""
        query = """ UPDATE  update_log SET last_updated = now() """
        self._db.modify_one(query, '')

    def insert_bill_desc(self, tups):
        """inserting bill descriptions to database"""
        query = """ INSERT INTO bills(bill_id, session_id,
            official_id, title, state, descr) VALUES (%(bill_id)s, %(session_id)s,
        %(number)s, %(title)s, %(state)s, %(description)s) """
        self._db.modify_many(query, tups)

    def insert_bill_log(self, tups):
        """inserting bill logs to database"""
        query = """ INSERT INTO bill_log(bill_id, status_date,
            status, last_action_date, last_action) VALUES (%(bill_id)s, %(status_date)s,
        %(status)s, %(last_action_date)s, %(last_action)s) """
        self._db.modify_many(query, tups)

    def insert_bills(self, desc, log):
        """insert all bill data to database"""
        self.insert_bill_desc(desc)
        self.insert_bill_log(log)

    def insert_session_data(self, tups):
        """insert new session data into database"""
        query = """ INSERT INTO sessions(session_id, year_start,
        year_end, session) VALUES (%(session_id)s, %(year_start)s,
        %(year_end)s, %(session)s) """
        self._db.modify_many(query, tups)
