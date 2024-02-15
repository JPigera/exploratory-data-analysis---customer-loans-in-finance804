import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect
import psycopg2


class RDSDatabaseConnector:

    def __init__(self, creds: dict):
        self.creds = creds

    def db_engine(self):

        with open(self.creds, 'r') as file:
            self.creds_dict = yaml.safe_load(file)
    
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = self.creds_dict['RDS_HOST']
        USER = self.creds_dict['RDS_USER']
        PASSWORD = self.creds_dict['RDS_PASSWORD']
        PORT = 5432
        DATABASE = self.creds_dict['RDS_DATABASE']
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        return engine
    
    def get_table_names(self, engine):

        inspector = inspect(engine)

        return inspector.get_table_names()
    
    def extract_data(self, engine):

        loan_payments_table = pd.read_sql('loan_payments', engine)

        return loan_payments_table
    
    def save_data(self, loan_payments_table):

        loan_payments_table.to_csv('df.csv')

        return
    
    def show_data(self, loan_payments_table):
        
        

        data_frame = pd.DataFrame(data=loan_payments_table)

        pd.set_option('display.max_rows', 4)

        pd.set_option('display.max_columns', None)

        print(data_frame)
        
        return
    

test = RDSDatabaseConnector('credentials.yaml')

engine= test.db_engine()

table_names = test.get_table_names(engine)

print(table_names)

loan_payments_table = test.extract_data(engine)

test.save_data(loan_payments_table)

test.show_data(loan_payments_table)