
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from databaseUtil import DatabaseUtil

# every table'ENGINE must be InnoDB in order to use mysql transaction

class Transaction:
  def __init__(self, conn):
    self.conn = conn
    self.queries = []
    self.dbUtil = DatabaseUtil()


  def addQuery(self, query, params):
    self.queries.append({ "query" : query, "params" : params})  


    # record is a dictionnary
  def addInsertQuery(self, tableName, record):
    rqt = self.dbUtil.formatInsert(tableName, record)
    self.queries.append(rqt)


  def addUpdateQuery(self, tableName, record, key, val):
    rqt = self.dbUtil.formatUpdate(tableName, record, key, val)
    self.queries.append(rqt)


  def addDeleteQuery(self, tableName, key, value):
    rqt = self.dbUtil.formatDelete(tableName, key, value)
    self.queries.append(rqt)


  def execute(self):
    self.conn.autocommit = 0
    cursor = self.conn.cursor()
    try:
      # execute each query
      for rqt in self.queries:
        cursor.execute(rqt['query'], rqt['params'])

      #Commit your changes
      self.conn.commit()
      return True
    except mysql.connector.Error as error :
      self.conn.rollback()
      print("Failed to update record to database rollback: {}".format(error))
      return False
    finally:
      cursor.close()
