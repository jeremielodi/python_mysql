from db.database import Database
import uuid

# 
_db = Database()

clientData =  {
  "name" : "yannick122",
  "dateOfBirth" : "2019-12-05",
  "age" : 78,
  "height" : 1.60,
  "uuid" : _db.bid('CCC4D7BA4F3B4BB783D29B89830855A8')
}

clientUpdateData =  {
  "name" : "Jeanus",
  "age" : 24
}

trans = _db.transaction()
trans.addUpdateQuery('client', clientUpdateData, 'id', 20)

trans.addInsertQuery('client', clientData)
#trans.addUpdateQuery('client', clientUpdateData, 'id', 5)
#trans.addDeleteQuery('client', 'id', 8)

transResult = trans.execute()
print(_db.execTrue(transResult))