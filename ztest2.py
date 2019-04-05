from database import Database

db = Database()
clients = db.exec('SELECT HEX(uuid)  as uuid, name, age FROM client')
print(clients)
