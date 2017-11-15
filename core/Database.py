#BEGIN IMPORT SYSTEM
from __future__ import print_function
import datetime
from shutil import copy2  # copy function to backup database
# Database:
import pandas as pd
from sqlalchemy import create_engine
#END IMPORT SYSTEM


#BEGIN IMPORT MINE
from logger import * # get all utils
from settings import settings
#END IMPORT MINE

log=Logger()

class simpleAPI():
    def __init__(self,**kwargs):
        '''Class to manage the Index Database'''
        self.DatabaseIndex = DatabaseHandler()
        self.load_sql()

        self.settings = {
            'ignore_headers': ['realpath'],
            'convert': {
                'moddate': ['unix', 'date']  # input output
            },
        }
        self.settings.update(settings['Database']['formated_data'])  # update with default settings

    def load_sql(self):
        """loads the data from sql database"""
        self.df     = self.DatabaseIndex.get_df_TableMain()

    def get_columns(self):
        '''get Columns of Dataframe'''
        return list(self.df.columns)  # [str(i) for i in self.df.columns]

    def get_header_formated(self):
        '''get the Header in formated form'''
        header = self.get_columns()
        for i in self.settings['ignore_headers']: header.remove(i)
        return header

    def get_table_convert(self):
        """Returns the table in converted form (without ignore_headers)
        :return: df.values
        """
        header = self.get_header_formated()
        df = self.df.loc[:, header]

        def transform_date(x):
            return datetime.datetime.fromtimestamp(float(x)).strftime("%Y/%m/%d")

        for key in self.settings['convert'].keys():
            if key in header:
                if key == 'moddate':
                    df[i] = df[i].apply(transform_date)
        return df.values

class DatabaseHandler():
    def __init__(self, **kwargs):
        '''Class to manage the Database'''

        self.defaults = {
            'db': 'tmp.db',  # Database to use
            'db_backup': True,  # should i backup the database.db
            'keys': ['id_db'],  # ID field
            'db_table_names': {  # names for tables
                'main': 'main',  # main table
                'keywords': 'keywords',  # keywords table
            }
        }
        self.defaults.update(settings['Database'])  # update with default settings

        # set defaults
        for k, v in self.defaults.iteritems(): setattr(self, k, v)

        # set kwargs
        self.kwargs = kwargs
        for k, v in kwargs.iteritems(): setattr(self, k, v)

    def db_do_backup(self, db, db_back=None):
        '''backup a Database'''
        if db_back is None: db_back = db + ".bck"
        copy2(db, db_back)  # shutil.copy2(src,dst)

    def db_sql_to_df(self,db=None, table=None):
        '''Loads in Database from SQL'''
        if db is None: db=self.db
        if table is None: table=self.db_table_names['DataIndex']

        engine = create_engine('sqlite:///{}'.format(db))  # starts the sqlite engine
        #FIXME ?? read_sql or read_sql_table ??
        df = pd.read_sql_table(table,engine,index_col='index')  # get the dataframe
        log("Loaded Dataframe from {}".format(db))
        return df

    def get_df_TableMain(self):
        """get the main table"""
        return self.db_sql_to_df(table=self.db_table_names['main'])

    def get_df_TableKeywords(self):
        """get the keywords table"""
        return self.db_sql_to_df(table=self.db_table_names['keywords'])

if __name__ == '__main__':
    DBAPI=simpleAPI()
    print("DBAPI.get_columns()",DBAPI.get_columns())
    print("DBAPI.get_header_formated()", DBAPI.get_header_formated())
    print("DBAPI.get_table_convert()")
    print(DBAPI.get_table_convert())