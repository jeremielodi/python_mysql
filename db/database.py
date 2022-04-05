import mysql.connector
import uuid
from .util import Util
from .transaction import Transaction
from .query_result import QueryResult

class Database:

    def __init__(self):
        # creating a mysql connection
        self.conn = self.createConnection()
        self.util = Util()

    def createConnection(self):
        if((not hasattr(self, 'conn')) or (not self.conn.is_connected())):
            self.conn = mysql.connector.connect(
                host="localhost",  # host
                user="root",  # use your mysql user name
                passwd="",  # use your mysql user passworsd
                port=3306,
                database="gestion")
        return self.conn

    
    # selection data from database

    def select(self, sql,  values=[]):
        rs = QueryResult()
        rs.status = False  # result
        try:
            mycursor = self.conn.cursor()
            sql = sql.replace("?", "%s")
            mycursor.execute(sql, values)
            values = mycursor.fetchall()
            colums = mycursor.column_names
            rs.status = True
            rs.rows = self.util.bind_keys_values(colums, values)
            return rs;
        except mysql.connector.Error as error:
            rs.msg = error.__dict__.get('_full_msg')
            rs.error_number = error.__dict__.get('errno')
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
        except (mysql.connector.Error, RuntimeError, TypeError, NameError) as error:
            rs.msg= error.__dict__.get('_full_msg')
            rs.error_number = error.__dict__.get('errno') or None
            return rs;
        finally:
            mycursor.close()


    # add(insert) or update data in the database

    def executeUpdate(self, sql, values=[]):
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

    # generate a uniq key, a binary key

    def uuid(self):
        return uuid.uuid4().bytes

    # convert string value to binary

    def bid(self, _val):
        return uuid.UUID(_val).bytes

    # convert data keys to binary, data is an array

    def convert(self, data, keys):
        for k in keys:
            if hasattr(data, k):
                data[k] = self.bid(data[k])
        return data

    # check if a select query was exceuted succefully
    def execTrue(self, rows):
        return not isinstance(rows, dict)

    # check if an insert, delete or update query was exceuted succefully
    def updatedTrue(self, result):
        return result.get('status')

    # close the connection with mysql
    def close(self):
        if(self.conn.is_connected()):
            self.conn.close()
