#Here we import only the neccessary modules

import yaml
import pandas as pd
from sqlalchemy import create_engine, inspect

'''
The following is a class to connect to an RDS database and extract a loan payments dataframe and save it into a csv file
'''

class RDSDatabaseConnector:

    '''
    Here we initialise the class with the only input needed is the 'credentials', which includes the details needed to access the RDS database
    
    '''

    def __init__(self, creds: dict):
        self.creds = creds

    '''
    The db_engine method is there to open the credentials file that is input by the user
    It extracts the various credentials and uses it to open the file; saving the out put into the engine variable
    The engine variable can be thought of as a key to access the database
    '''

    def db_engine(self):

        with open(self.creds, 'r') as file: #opening the yaml file input and creating an instance of the class in the variable self.creds_dict variable
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
    
    '''
    The get_table_names does what it says on the tin, it gets the table names
    We use the built in inspect function from the sqlalchemy library to inspect the whole database
    Then the get_table_names() function returns a list of table names
    '''
    
    def get_table_names(self, engine):

        inspector = inspect(engine)

        return inspector.get_table_names()
    
    '''
    'loan payments' is the table we're looking for
    We use the engine along with the built in read_sql() function from the pandas library to assign the table to the variable 'loan_payments_table'
    '''
    
    def extract_data(self, engine):

        loan_payments_table = pd.read_sql('loan_payments', engine)

        return loan_payments_table
    
    ''''
    Now we can save that table to a csv file using the save_data() method
    '''
    
    def save_data(self, loan_payments_table):

        loan_payments_table.to_csv('df.csv')

        return
    
    '''
    To have an idea about what the data looks like,
    the show_data() method shows a snippet of the table with all the columns and a small number of rows
    '''
    
    def show_data(self, loan_payments_table):

        data_frame = pd.DataFrame(data=loan_payments_table)

        pd.set_option('display.max_rows', 30)

        pd.set_option('display.max_columns', None)

        print(data_frame)
        
        return
    
class DataTransform:

    def __init__(self, loan_payments_table):

        self.loan_payments_table = loan_payments_table

    def check_id_unique(self):
        
        num_unique_ids = loan_payments_table['id'].nunique()

        row_count = len(loan_payments_table)

        if num_unique_ids == row_count:
            print("All id's are unique")
        else:
            print("Not all of the id's are unique")

        return

    def str_to_int(self):

        self.loan_payments_table['term'].str.replace('36 months', '36').astype(int)

        return
        


'''
Here we test the class by first running an instance of the class under the variable 'test' and the input of our locally stored credentials.yaml file
Then we can run our methods from the test instance
'''

test = RDSDatabaseConnector('credentials.yaml')

engine= test.db_engine() #get the key to the database using the credentials

table_names = test.get_table_names(engine) #use the key to get the table names

print(table_names) #view the table names

loan_payments_table = test.extract_data(engine) #use the key to access the loan payments table

# test.show_data(loan_payments_table) # show a snippit of the data

# transform = DataTransform(loan_payments_table)

# check_id = transform.check_id_unique()

# term_months_into_years = transform.str_to_int()

test.save_data(loan_payments_table) #save the loan payments table to the csv file