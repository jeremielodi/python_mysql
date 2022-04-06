from settup_env import EnvironementSettup
EnvironementSettup();
from db.database import Database

_db = Database()

if _db.conn_status :

    clientData = {
        #"id": 1,
        "name": "Massamba k",
        "dateOfBirth": "1979-07-08",
        "age": 78,
        "height": 1.60,
        "uuid": _db.bid('CCC4D7BA4F3B4BB783D29B89830855A8')
    }

    clientUpdateData = {
        "name" : "Jeancy"
    }

    Result = _db.insert('client', clientData)

    
    print(Result.status, Result.affected_rows, Result.error_number, Result.msg)

    # to get the last inserted id : Result['lastrowid'][0]


    #    delete example
    # ....................
    # you cand change @age to id, it's just a condition

    # _db.delete('client','age', 78)

    #    update example
    # ...................................
    # you cand change @age to id, it's just a condition

    # _db.update('client', clientUpdateData,  'age', 78)
