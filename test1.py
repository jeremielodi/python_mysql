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

result = _db.insert('client', clientData)

success = result.get('status')

print(success, result)
