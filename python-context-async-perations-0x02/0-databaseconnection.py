import sqlite3

# custom contect manager class
class DatabaseConnection:
    def __init__(self,db_path):
        self.db_path = db_path
        self.conn = None
        
    def __enter__(self):
        # this usually runs at start of with block
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        # this runs when exiting the with block
        if self.conn:
            self.conn.close()

# usage
if __name__ == "__main__":
    with DatabaseConnection("test.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        for row in results:
            print(row)