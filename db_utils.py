import yaml
import pandas as pd

class RDSDatabaseConnector:

    def readcreds():
        with open('credentials.yaml', 'r') as file:
            creds = yaml.safe_load(file)
        return creds

    def __init__(self, creds: dict):
        self.creds = self.readcreds()

    def create_engine(self):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = self.creds['RDS_HOST']
        USER = self.creds['RDS_USER']
        PASSWORD = self.creds['RDS_PASSWORD']
        PORT = 5432
        DATABASE = self.creds['RDS_DATABASE']
        engine = self.create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        return engine
    
    def extractdata():
        self.data = self.pandas.read_sql()
        return self.data