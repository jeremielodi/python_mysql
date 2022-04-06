from settup_env import EnvironementSettup
EnvironementSettup();

from  db.filterParser import FilterParser
from db.database import Database


sqlSource = '''
  SELECT c.id, c.name, c.dateOfBirth
  FROM client c
'''
# specify here fields to compare
options = {
  "limit" : 12,
  "name" : "yannick122",
  "dateOfBirth" : '2019-12-05'
}

filter = FilterParser(options, { "tableAlias" : 'c' })
filter.equals("id")
filter.equals("name")
filter.dateFrom('dateOfBirth')

sql = filter.applyQuery(sqlSource)
params = filter.parameters()

_db = Database()

clients = _db.select(sql, params)

print(clients.rows)