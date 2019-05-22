from db.database import Database
import uuid


# 
_db = Database()

clientData =  {
  "name" : "Kasongo",
  "dateOfBirth" : "1979-07-08",
  "age" : 78,
  "height" : 1.60,
  "uuid" : _db.bid('CCC4D7BA4F3B4BB783D29B89830855A8')
}

result = _db.insert('client', clientData) 

print(_db.updatedTrue(result), result)
