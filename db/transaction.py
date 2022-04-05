import mysql.connector
from mysql.connector import Error, errorcode
from .util import Util

# every table'ENGINE must be InnoDB in order to use mysql transaction


class Transaction:

    def __init__(self, conn):
        self.conn = conn
        self.queries = []
        self.util = Util()

    # add more query for the transactions
    def add_query(self, query, params):
        self.queries.append({"query": query, "params": params})

    # add more query for the transactions
    # record is a dictionnary
    def add_insert_query(self, tableName, record):
        rqt = self.util.format_insert(tableName, record)
        self.queries.append(rqt)

    # add more query for the transactions
    # and update query
    def add_update_query(self, tableName, record, key, val):
        rqt = self.util.format_update(tableName, record, key, val)
        self.queries.append(rqt)

    # add more query for the transactions
    # a delete query
    def add_delete_query(self, tableName, key, value):
        rqt = self.util.format_delete(tableName, key, value)
        self.queries.append(rqt)

    # excute all queries
    def execute(self):
        result = []
        rs = {'status': False}  # responses
        self.conn.autocommit = False
        cursor = self.conn.cursor()
        try:
            # execute each query
            for rqt in self.queries:

                sql = rqt['query'].replace("?", "%s")
                params = rqt['params']
                cursor.execute(sql, params)
                result.append(
                    {
                        'lastrowid': cursor.lastrowid or None,
                        'affectedRows':  cursor.rowcount or None
                    })
            self.conn.commit()
            # Commit your changes

            return result
        except mysql.connector.Error as error:
            print(error)
            self.conn.rollback()
            rs['msg'] = format(error)
            return rs
        finally:
            if(self.conn.is_connected()):
                cursor.close()
