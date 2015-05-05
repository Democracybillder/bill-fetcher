#!/usr/bin/python
'''db layer for state bill fetcher'''
import psycopg2

class DB(object):
    """db wrapper"""
    _db_connection = None
    _db_cur = None
    _db_name = "billder"

    def __init__(self):
        self._db_connection = psycopg2.connect(dbname=self._db_name)
        self._db_cur = self._db_connection.cursor()

    def modify_many(self, query, params):
        """insert or update multiple rows"""
        return self._db_cur.executemany(query, params)

    def modify_one(self, query, params):
        """ insert or update one row """
        return self._db_cur.execute(query, params)

    def select(self, query, params):
        """ select rows """
        self._db_cur.execute(query, params)
        rows = self._db_cur.fetchall()
        return rows

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()

class BillDB(object):
    """ database logic """
    _db = None
    def __init__(self):
        self._db = DB()

    def getlastdbmodification(self):
        """ fetching the last timestamp of data modification from the db"""
        query = """ SELECT MAX(last_updated) FROM update_log """
        return self._db.select(query, '')

    def updatelastdbmodification(self):
        """ updating the last timestamp of data modification in the db"""
        query = """ UPDATE  update_log SET last_updated = now() """
        self._db.modify_one(query, '')

    def insertbilldesc(self, tups):
        """inserting bill descriptions to database"""
        query = """ INSERT INTO bills(bill_id, session_id,
            official_id, title, state, descr) VALUES (%(bill_id)s, %(session_id)s,
        %(number)s, %(title)s, %(state)s, %(description)s) """
        self._db.modify_many(query, tups)

    def insertbilllog(self, tups):
        """inserting bill logs to database"""
        query = """ INSERT INTO bill_log(bill_id, status_date,
            status, last_action_date, last_action) VALUES (%(bill_id)s, %(status_date)s,
        %(status)s, %(last_action_date)s, %(last_action)s) """
        self._db.modify_many(query, tups)

    def insertbills(self, desc, log):
        """insert all bill data to database"""
        self.insertbilldesc(desc)
        self.insertbilllog(log)

    def insertsessiondata(self, tups):
        """insert new session data into database"""
        query = """ INSERT INTO sessions(session_id, year_start,
        year_end, session) VALUES (%(session_id)s, %(year_start)s,
        %(year_end)s, %(session)s) """
        self._db.modify_many(query, tups)


