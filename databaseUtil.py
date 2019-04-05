class DatabaseUtil :

    
  def escape(self, val):
    if type(val) == bytes :
      return val
    else:
      return str(val)

  #data should a dictionnary
  def formatInsert(self, tableName, data):
    cols = ""
    vals = ""
    keys = data.keys()
    nCol = len(keys)
    record = []
    i = 1
    for k in keys:
      cols = cols + ""+k+""
      vals = vals + "%s"
      record.append(self.escape(data[k]))
      
      if i != nCol:
        cols = cols+ " ,"
        vals = vals + " ,"
      i = i + 1

      sql = "INSERT INTO "+ tableName +"("+cols+") VALUES("+vals+")" + ";"
    return { "query" : sql, "params" : record}
  
    #data should a dictionnary
  def formatUpdate(self, tableName, data, key, value):
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
    sql = "UPDATE "+ tableName + " SET " + vals + " WHERE "+ key + "=%s"
    return { "query" : sql, "params" : record }

  def formatDelete(self, tableName, key, value):
    sql = "DELETE FROM "+ tableName + " WHERE " + key + "=%s"
    return { "query" : sql, "params" : [self.escape(value)] }