import os
import uuid

from db.query_result import QueryResult
db_type = os.getenv('DB_TYPE')

if db_type == 'postgres':
    from db.pg import Database as DB
elif db_type == 'mysql':
    from db.mysql import Database as DB
else :
    raise ValueError('Invalid database type, fixe .env DB_TYPE variable')

class Database(DB) :
    def __init__(self):
        super().__init__()
        
    
    def select(self,  sql,  values=[]) :
        return self.toResult(super().select(sql, values));

    def insert(self, tableName, record) :
        return self.toResult(super().save(tableName, record));

    def one(self,  sql,  values=[]) :
        return self.toResult(super().one( sql,  values));

    def update(self,  tableName, record, key, value) :
        return self.toResult(super().update(tableName, record, key, value));

    def delete(self,  tableName, key, value) :
        return self.toResult(super().delete(tableName, key, value));

    def transaction(self):
        return super().transaction()
    # generate a uniq key, a binary key
    def uuid(self):
        return uuid.uuid4().bytes

    # generate a uniq key, a String key
    def uuid_string(self):
        return uuid.uuid4()

    # convert string value to binary

    def bid(self, _val):
        return uuid.UUID(_val).bytes
    
    # convert data keys to binary, data is an array

    def convert(self, data, keys):
        for k in keys:
            if hasattr(data, k):
                data[k] = self.bid(data[k])
        return data

    def toResult(self, rs):
        qrs = QueryResult();
        return qrs.from_obj(rs)
    
    def status(self):
        return self.conn_status;