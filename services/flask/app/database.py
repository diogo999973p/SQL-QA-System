import dataset

class Database:
    def __init__(self, username, password, database):
        connection_string = f'mssql+pyodbc://{username}:{password}@sqlserver:1433/{database}?driver=ODBC+Driver+17+for+SQL+Server'
        self.conn = dataset.connect(connection_string, schema='production')

    def execute_query(self, query):
        result = self.conn.query(query)
        return result