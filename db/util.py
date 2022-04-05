
from hashlib import sha1
from datetime import datetime, date

class Util :

  def escape(self, val):
    if type(val) == bytes :
      return val
    else:
      return str(val)


  #data should a dictionnary
  def format_insert(self, tableName, data):
    cols = ""
    vals = ""
    keys = data.keys()
    nCol = len(keys)
    record = []
    i = 1
    for k in keys:
      cols = cols + "" + k + ""
      vals = vals + "%s"
      record.append(self.escape(data[k]))
      
      if i != nCol:
        cols = cols + " ,"
        vals = vals + " ,"
      i = i + 1

      sql = "INSERT INTO " + tableName + "(" + cols + ") VALUES(" + vals + ")" + ";"
    return { "query" : sql, "params" : record }


    #data should a dictionnary
  def format_update(self, tableName, data, primaryKey, value):
    vals = ""
    keys = data.keys()
    nCol = len(keys)
    record = []
    i = 1
    for k in keys:
      vals = vals + k +" = %s"
      record.append(self.escape(data[k]))
      
      if i != nCol:
        vals = vals + " ,"
      i = i + 1
    # add the key's value into parameters
    record.append(self.escape(value))
    sql = "UPDATE " + tableName + " SET " + vals + " WHERE " + primaryKey + "=%s"
    return { "query" : sql, "params" : record }


  def format_delete(self, tableName, key, value):
    sql = "DELETE FROM " + tableName + " WHERE " + key + "=%s"
    return { "query" : sql, "params" : [self.escape(value)] }
 

  def bind_keys_values(self, keys, values):
    rows = []
    for r in values:
        record = {}
        j = 0
        for col in keys:
          record[col] = self.format_field(r[j])
          j = j + 1
        rows.append(record)
    return rows

  def to_sha1(self, value):
    sha_1 = sha1()
    sha_1.update(value.encode('utf8'))
    return sha_1.hexdigest()
  
  def is_decimal(self, value) :
        try :
          float(value)
          return True
        except :
          pass
        return False;
  
  def format_field(self, value) :
    if  type(value) is date or type(value) is datetime:
      return f"{value}"
    elif  type(value) is int:
      return value
    elif self.is_decimal(value) :
      return float(value)
    else :
      return value
