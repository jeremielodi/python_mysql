import json
class QueryResult:
    
    def __init__(self) :
        self.status = False;
        self.msg = '';
        self.affected_rows = 0;
        self.lastrowid = None;
        self.error_number = '';
        self.rows = []
        self.record = None
        
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