#!/usr/bin/python
'''db access wrapper'''

import psycopg2

class DB(object):
    """db wrapper"""
    _db_connection = None
    _db_cur = None
    # db connection details
    _db_host = None
    _db_user = None
    _db_passwd = None
    _db_name = None

    def __init__(self, conf):
        """initializing a db wrapper object
        by reading connection details from configuration object"""
        #assigning connection params
        self._db_host = conf["postgres"]["host"]
        self._db_user = conf["postgres"]["user"]
        self._db_passwd = conf["postgres"]["passwd"]
        self._db_name = conf["postgres"]["db"]

        # creating connection
        self._db_connection = psycopg2.connect(database=self._db_name,
            user=self._db_user, password=self._db_passwd, host=self._db_host)
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
        """ gracefully terminating db connection """
        self._db_cur.close()
        self._db_connection.close()
