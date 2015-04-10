#!/usr/bin/python
'''db layer for state bill fetcher'''
import psycopg2


class FetcherDb(object):
    """database class"""
def __init__(self, dbname):
    self.dbname = dbname

def dbinserttuple(self, query, tup):
    """wrapper method to handle db connections and tuple inserts"""
    conn = psycopg2.connect(dbname=self.dbname)
    cur = conn.cursor()
    cur.executemany(query, tup)
    return conn.commit()

def insertbilldesc(self, tups):
    """inserting bill descriptions to database"""
    query = """ INSERT INTO bills(bill_id, session,
        official_id, title, "desc") VALUES (%(bill_id)s, %(session)s,
    %(number)s, %(title)s, %(description)s) """
    return dbinserttuple(self.dbname, query, tups)


def insertbilllog(self, tups):
    """inserting bill logs to database"""
    query = """ INSERT INTO bill_log(bill_id, status_date,
        status, last_action_date, last_action) VALUES (%(bill_id)s, %(status_date)s,
    %(status)s, %(last_action_date)s, %(last_action)s) """
    return dbinserttuple(self.dbname, query, tups)

def insertbills(self, desc, log):
    """insert all bill data to database"""
    return insertbilldesc(self.dbname, desc), insertbilllog(self.dbname, log)




