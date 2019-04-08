from db.database import Database
from db.period import PeriodService

_db = Database()

clients = _db.select('''
    SELECT id, name, dateOfBirth, height, age 
    FROM clients
''')
# clients should be an list(array) not a dict (json)
success = not isinstance(clients, dict)

print(success)
print(clients)

