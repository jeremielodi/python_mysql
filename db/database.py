import mysql.connector
import uuid
from db.util import Util
from db.transaction import Transaction

class Database :

  def __init__(self):
    # creating a mysql connection
    self.conn = mysql.connector.connect(
      host = "localhost", # host
      user = "root", # use your mysql user name
      passwd = "", # use your mysql user passworsd
      database = "gestion")
    self.util = Util()


  # selection data from database
  def select(self, sql, params = []):
    return self.exec(sql, params)


  # record is a dictionnary
  def insert(self, tableName, record):
    rqt = self.util.formatInsert(tableName, record)
    return self.execute(rqt['query'], rqt['params'])


  # record is a dictionnary
  def update(self, tableName, record, key, value):
    rqt = self.util.formatUpdate(tableName, record, key, value)
    return self.execute(rqt['query'], rqt['params'])


  # delete record in the database
  def delete(self, tableName, key, value):
    rqt = self.util.formatDelete(tableName, key, value)
    return self.execute(rqt['query'], rqt['params'])


  # add(insert) or update data in the database
  # return { status, lastrowid, msg }

  def execute(self, sql, values = []):
    mycursor = self.conn.cursor()
    rs =  { 'status' : False } # result
    try:
      sql = sql.replace("?", "%s")
      mycursor.execute(sql, values)
      self.conn.commit()
      rs['status'] = True
      rs['lastrowid'] = mycursor.lastrowid or None,
      rs['affectedRows'] = mycursor.rowcount or None

    except mysql.connector.Error as error :

      rs['msg'] = error.__dict__.get('_full_msg')
      rs['errno'] = error.__dict__.get('errno')

    finally:
      mycursor.close()
      return rs


  # add(insert) or update data in the database
  def executeUpdate(self, sql, values = []):
    return self.execute(sql, values)


  # select rows from the database
  # return an array(list) is the request is well executed
  # return a dist when something o wrong
  def exec(self, sql,  values = []):
    rs =  { 'status' : False } # result
    try:
      mycursor = self.conn.cursor()
      sql = sql.replace("?", "%s")
      mycursor.execute(sql, values)
      values = mycursor.fetchall()
      colums = mycursor.column_names
      return self.util.bindKeysValues(colums, values)

    except mysql.connector.Error as error :
      rs['msg'] = error.__dict__.get('_full_msg')
      rs['errno'] = error.__dict__.get('errno')
      return rs
    finally:
      mycursor.close()
     


  #retrieve the first record from the result
  def one(self, sql, params):
    rows = self.exec(sql, params)
    if len(rows) > 0:
      return rows[0]
    else:
      return False

  #transaction 
  def transaction(self):
    return Transaction(self.conn)

  # return connection property
  def connection(self):
    return self.conn


  # generate a uniq key
  def uuid(self):
    return uuid.uuid4().bytes


  # convert string val to binary
  def bid(self, _val):
    return uuid.UUID(_val).bytes
  

  # convert data keys to binary
  def convert(self, data, keys):
    for k in keys:
      if hasattr(data, k) :
        data[k] = self.bid(data[k])
    return data
