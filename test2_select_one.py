from settup_env import EnvironementSettup
EnvironementSettup();

from db.database import Database

_db = Database()

if _db.conn_status :

    clients = _db.one('''
        SELECT id, name, dateOfBirth, height, age 
        FROM client
        WHERE id=?
    ''', ["4"])

    Result = clients;
    # print(Result.status, Result.rows, Result.error_number, Result.msg)
    print(Result.rows)
