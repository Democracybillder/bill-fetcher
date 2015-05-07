#!/usr/bin/python
'''db access wrapper'''

import psycopg2

class DB(object):
    """db wrapper"""
    _db_connection = None
    _db_cur = None

    # db connection details
    _db_conf = None


    def __init__(self, conf):
        """initializing a db wrapper object
        by reading connection details from configuration object"""

        self._db_conf = conf
        # creating connection
        self._db_connection = psycopg2.connect(
            database=self._db_conf["db"],
            user=self._db_conf["user"],
            password=self._db_conf["passwd"],
            host=self._db_conf["host"])

        self._db_cur = self._db_connection.cursor()

    def modify_many(self, query, params):
        """insert or update multiple rows"""
        print 'query =', query, 'params =', params
        assert False
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
