#!/usr/bin/python
'''db layer for state bill fetcher'''
import psycopg2




def dbinserttuple(dbname, query, tup):
    """wrapper method to handle db connections and tuple inserts"""
    conn = psycopg2.connect(dbname=dbname)
    cur = conn.cursor()
    cur.executemany(query, tup)
    conn.commit()
    cur.close()
    conn.close()

def dbselect(dbname, query):
    """wrapper method to handle db connections and selects"""
    conn = psycopg2.connect(dbname=dbname)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def getlastdbmodification(dbname):
    """ fetching the last timestamp of data modification from the db"""
    query = """ SELECT MAX(last_updated) FROM update_log """
    return dbselect(dbname, query)

def updatelastdbmodification(dbname, date):
    """ updating the last timestamp of data modification in the db"""
    query = """ UPDATE  update_log SET last_updated = %s """
    dbinserttuple(dbname, query, date)

def insertbilldesc(dbname, tups):
    """inserting bill descriptions to database"""
    query = """ INSERT INTO bills(bill_id, session,
        official_id, title, state, "desc") VALUES (%(bill_id)s, %(session)s,
    %(number)s, %(title)s, %(state)s, %(description)s) """
    dbinserttuple(dbname, query, tups)


def insertbilllog(dbname, tups):
    """inserting bill logs to database"""
    query = """ INSERT INTO bill_log(bill_id, status_date,
        status, last_action_date, last_action) VALUES (%(bill_id)s, %(status_date)s,
    %(status)s, %(last_action_date)s, %(last_action)s) """
    dbinserttuple(dbname, query, tups)


def insertbills(dbname, desc, log):
    """insert all bill data to database"""
    insertbilldesc(dbname, desc)
    insertbilllog(dbname, log)


