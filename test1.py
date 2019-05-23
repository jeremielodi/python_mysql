from db.database import Database
#

_db = Database()

clientData = {
    "name": "Kasongo",
    "dateOfBirth": "1979-07-08",
    "age": 78,
    "height": 1.60,
    "uuid": _db.bid('CCC4D7BA4F3B4BB783D29B89830855A8')
}

clientUpdateData = {
    "name" : "Jeancy"
}

Result = _db.save('client', clientData)

# _db.updatedTrue tells you if your request has been excuted succefully
print(_db.updatedTrue(Result), Result)



#    delete example
# ....................
# you cand change @age to id, it's just a condition

# _db.delete('client','age', 78)



#    update example
# ...................................
# you cand change @age to id, it's just a condition

# _db.update('client', clientUpdateData,  'age', 78)
