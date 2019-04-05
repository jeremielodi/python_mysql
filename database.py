# sqlalchemy

import mysql.connector
import uuid
from databaseUtil import DatabaseUtil
from transaction import Transaction

class Database :
  
  def __init__(self):

    self.conn = mysql.connector.connect(
      host = "localhost",
      user = "congoschool",
      passwd = "congos@drc#2017",
      database = "gestion"
    )
    self.dbUtil = DatabaseUtil()

  # insert or update data in the database
  def execute(self, sql, values = ()):
    mycursor = self.conn.cursor()
    try:
      mycursor.execute(sql, values)
      self.conn.commit()
      return True
    except mysql.connector.Error as error :
      print("Failed to update record to database rollback: {}".format(error))
      return False
    finally:
      mycursor.close()


  # select rows from the database
  def exec(self, sql):
    mycursor = self.conn.cursor()
    mycursor.execute(sql)
    result = []
    mycursor.with_rows
    for r in mycursor.fetchall():
      line = {}
      j = 0
      for col in mycursor.column_names:
        line[col] = r[j]
        j = j + 1
      result.append(line)
    mycursor.close()
    return result



  # record is a dictionnary
  def insert(self, tableName, record):
    rqt = self.dbUtil.formatInsert(tableName, record)
    return self.execute(rqt['query'], rqt['params'])

  # record is a dictionnary
  def update(self, tableName, record, key, value):
    rqt = self.dbUtil.formatUpdate(tableName, record, key, value)
    return self.execute(rqt['query'], rqt['params'])

  def delete(self, tableName, key, value):
    rqt = self.dbUtil.formatDelete(tableName, key, value)
    return self.execute(rqt['query'], rqt['params'])
  
  #transaction 
  def transaction(self):
    return Transaction(self.conn)

  def connection(self):
    return self.conn

  # generate a uniq key
  def uuid(self):
    return uuid.uuid4().bytes

  def bid(self, _val):
    return uuid.UUID(_val).bytes
