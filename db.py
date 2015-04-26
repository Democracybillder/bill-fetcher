#!/usr/bin/python
'''db layer for state bill fetcher'''
import psycopg2


def dbinserttuple(dbname, query, tup):
    """wrapper method to handle db connections and tuple inserts"""
    conn = psycopg2.connect(dbname=dbname)
    cur = conn.cursor()
    cur.executemany(query, tup)
    conn.commit()

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

def insertsessiondata(dbname,sessions):
    """insert new session data into database"""
    query = """ INSERT INTO sessions(session_id, year_start,
        year_end, session) VALUES (%(session_id)s, %(year_start)s,
    %(year_end)s, %(session)s) """
    dbinserttuple(dbname, query, tups)
