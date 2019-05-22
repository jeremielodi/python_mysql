from db.database import Database
from db.period import PeriodService

_db = Database()

clients = _db.select('''
    SELECT id, name, dateOfBirth, height, age 
    FROM client
''')

print(_db.execTrue(clients))

print(clients)
