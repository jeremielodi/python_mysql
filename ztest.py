from database import Database
import uuid

import json

db = Database()
# 

clientData =  {
  "name":"yannick122",
  "dateOfBirth" : "2019-12-05",
  "age" : 78,
  "height" : 1.60,
  "uuid" : db.bid('CCC4D7BA4F3B4BB783D29B89830855A8')
}

clientUpdateData =  {
  "name":"Jeanus",
  "age" : 24
}

trans = db.transaction()
trans.addInsertQuery('client', clientData)
#trans.addUpdateQuery('client', clientUpdateData, 'id', 5)
#trans.addDeleteQuery('client', 'id', 8)

r = trans.execute() # True or False
print(r)
