from db.database import Database
from db.period import PeriodService
from settup_env import EnvironementSettup
#

EnvironementSettup();

_db = Database()

if _db.conn_status :

    clients = _db.select('''
        SELECT id, name, dateOfBirth, height, age 
        FROM client
    ''')

    Result = clients;
    # print(Result.status, Result.rows, Result.error_number, Result.msg)
    print(Result.rows)
