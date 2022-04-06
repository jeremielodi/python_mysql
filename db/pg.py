import psycopg2
from psycopg2 import pool
from .util import Util
from .query_result import QueryResult
import os

class Database:

    def __init__(self):
        # creating a pg connection
        self.conn_status = False
        self.conn = self.create_connection()
        self.util = Util()

    def create_connection(self):
        if((not hasattr(self, 'conn')) or (not self.conn.is_connected())):
            try:
                postgreSQL_pool = pool.SimpleConnectionPool(1, 20,
                    host = os.getenv("DB_HOST"),  # host
                    user = os.getenv('DB_USER'),  # use your pg user name
                    password = os.getenv('DB_PASS'),  # use your pg user passworsd
                    port = os.getenv('DB_PORT'),
                    database = os.getenv('DB_NAME'))
                self.conn = postgreSQL_pool.getconn()
                self.conn_status = True
                return self.conn
            except psycopg2.Error as error:
                self.conn_status = False
                result = { 
                    "status" : False,
                    "msg" : error.pgerror,
                    "error_number" : error.pgcode
                },
                print(result)
                return result
        return None 

    def connect(self):
        self.create_connection()

    # selection data from database

    def select(self, sql,  values=[]):
        rs = QueryResult()
        rs.status = False  # result
        try:
            mycursor = self.conn.cursor()
            sql = sql.replace("?", "%s")
            mycursor.execute(sql, values)
            values = mycursor.fetchall()
            colums = [desc[0] for desc in mycursor.description]
            rs.status = True
            rs.rows = self.util.bind_keys_values(colums, values)
            return rs;
        except psycopg2.Error as error:
            rs.msg = error.pgerror
            rs.error_number = error.pgcode
            return rs
        finally:
            mycursor.close()

    # record is a dictionnary

    def insert(self, tableName, record):
        rqt = self.util.format_insert(tableName, record)
        return self.execute(rqt['query'], rqt['params'])

    def save(self, tableName, record):
        return self.insert(tableName, record)

    # record is a dictionnary
    def update(self, tableName, record, key, value):
        rqt = self.util.format_update(tableName, record, key, value)
        return self.execute(rqt['query'], rqt['params'])

    # delete record in the database

    def delete(self, tableName, key, value):
        rqt = self.util.format_delete(tableName, key, value)
        return self.execute(rqt['query'], rqt['params'])

    # delete record in the database
    def remove(self, tableName, key, value):
        return self.delete(tableName, key, value)

    # add(insert) or update data in the database
    # return { status, lastrowid, msg }

    def execute(self, sql, values=[]):
        mycursor = self.conn.cursor()
        rs =  QueryResult()
        rs.status = False  # result
        try:
            sql = sql.replace("?", "%s")
            mycursor.execute(sql, values)
            self.conn.commit()
            rs.status = True
            rs.lastrowid = mycursor.lastrowid or None,
            rs.affected_rows = mycursor.rowcount or 0
            return rs;
        except psycopg2.Error as error:
            rs.msg= error.pgerror
            rs.error_number = error.pgcode
            return rs;
        finally:
            mycursor.close()


    # add(insert) or update data in the database

    def execute_update(self, sql, values=[]):
        return self.execute(sql, values)

    # select rows from the database
    # return an array(list) is the request is well executed
    # return a dist when something o wrong

    # retrieve the first record from the result

    def one(self, sql, params):
        result = self.select(sql, params)
        if len(result.rows) > 0 :
            result.record = result.rows[0]
        else :
            result.status = False;
        return result;        
        

    # start transaction

    def transaction(self):
        return Transaction(self.conn)

    # return connection property

    def connection(self):
        return self.conn

    # close the connection with postgres
    def close(self):
        if(self.conn.is_connected()):
            self.conn_status = False;
            self.conn.close()


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
                rs = QueryResult()
                rs.affected_rows = cursor.rowcount or None;
                rs.lastrowid =  cursor.lastrowid or None,
                result.append(rs)
            self.conn.commit()
            # Commit your changes
            return {
                "commited" : True,
                "results" : result
            }
        except (Exception, psycopg2.DatabaseError, psycopg2.Error) as error:
            self.conn.rollback()
            rs = QueryResult()
            rs.msg = error.pgerror
            rs.error_number = error.pgcode
            return {
                "commited" : False,
                "results" : [rs]
            }
        finally:
            cursor.close()
