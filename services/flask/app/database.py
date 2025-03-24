import dataset

class Database:
    def __init__(self, username, password, database):
        self.connection_string = f'mssql+pyodbc://{username}:{password}@sqlserver:1433/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        self.conn = None  # Connection is created only when needed
        
    def connect(self):
        if self.conn is None:
            self.conn = dataset.connect(self.connection_string, schema='production')
                    

    def execute_query(self, query):
        self.connect()
        result = self.conn.query(query)
        return result
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None