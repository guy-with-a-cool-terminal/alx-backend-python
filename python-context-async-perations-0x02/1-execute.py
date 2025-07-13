import sqlite3

class ExecuteQuery:
    def __init__(self,db_path,query,params=None):
        self.db_path = db_path
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.results = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        cursor.execute(self.query,self.params)
        self.results = cursor.fetchall()
        return self.results
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery("test.db", query, params) as results:
        for row in results:
            print(row)