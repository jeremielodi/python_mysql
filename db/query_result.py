import json
class QueryResult:
    
    def __init__(self) :
        # status tell you if the request has been executed succefully
        self.status = False;
        self.msg = '';
        self.affected_rows = 0;
        self.lastrowid = None;
        self.error_number = '';
        self.rows = []
        self.record = None

    def __setitem__(self, key, val):
        self[key] = val
        
    def from_obj(self, obj) :
        self.msg = obj.msg;
        self.affected_rows = obj.affected_rows;
        self.lastrowid = obj.lastrowid;
        self.error_number = obj.error_number;
        self.rows = obj.rows
        self.record = obj.record
        return self;

    def __str__(self) :
        return json.dumps({
            "status" : self.status,
            "msg": self.msg,
            "affectedRows" : self.affected_rows or 0,
            "lastRowId": self.lastrowid,
            "errorNumber" : self.error_number,
            "rows": self.rows,
            "record": self.record
        });