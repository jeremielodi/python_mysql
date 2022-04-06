from settup_env import EnvironementSettup
EnvironementSettup();
from db.database import Database

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

trans.add_update_query('client', clientUpdateData, 'age', 78)

trans.add_insert_query('client', clientData)
#trans.add_update_query('client', clientUpdateData, 'id', 5)
#trans.add_delete_query('client', 'id', 8)

transResult = trans.execute()

print(transResult['commited'],)
for r in transResult['results']:
  print(r)