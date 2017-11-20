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
        self.DatabaseHandler = DatabaseHandler()
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
        self.df     = self.DatabaseHandler.get_df_TableMain()

    def save_sql(self):
        """Save data to sql"""
        self.save_sql_TableMain()
        #self.save_sql_TableKeywords()
        # etc
        log.info("Saved Database")

    def save_sql_TableMain(self,db=None):
        """Save table Main"""
        self.DatabaseHandler.set_df_TableMain(self.df,db=None)

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

        # convert data
        def transform_date(x):
            return datetime.datetime.fromtimestamp(float(x)).strftime("%Y/%m/%d")

        for key in self.settings['convert'].keys():
            if key in header:
                if key == 'moddate':
                    df[i] = df[i].apply(transform_date)
        return df.values

    def get_entry(self,ID,header='formated'):
        """
        Function to get the entry to a ID
        :param ID: table index of the entry
        :param header: None,'formated',list
                    which columns one wants to have returned
                    None       :  return the entry to all columns
                    'formated' :  return the entry to for all beside ignored columns (default)
                    list       :  return the entry for all columns in the list
        :return: header, entry
        """

        if header is None:  # case we want the entry to all data
            header = self.get_columns()
        elif header == 'formated':  # default case
            header = self.get_header_formated()
        else:
            header = header

        df = self.df.loc[ID, header]

        # convert data
        def transform_date(x):
            return datetime.datetime.fromtimestamp(float(x)).strftime("%Y/%m/%d")

        for key in self.settings['convert'].keys():
            if key in header:
                if key == 'moddate':
                    df[i] = df[i].apply(transform_date)

        return header, df.values

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
        if table is None: table=self.db_table_names['main']

        engine = create_engine('sqlite:///{}'.format(db))  # starts the sqlite engine
        #FIXME ?? read_sql or read_sql_table ??
        df = pd.read_sql_table(table,engine,index_col='index')  # get the dataframe
        log("Loaded Dataframe from {}".format(db))
        return df

    def db_df_to_sql(self, df=None, db=None, table=None, *args, **kwargs):
        '''Saves Dataframe as SQL data'''

        if db is None: db = self.db
        if table is None: table = self.db_table_names['main']
        if df is None:
            if hasattr(self, 'df'):
                df = self.df
            else:
                raise StandardError("Cant save dataframe without a dataframe defined")
        defaults = {'if_exists': 'replace'}
        kwargs = dict(defaults, **kwargs)

        # Create new file
        if os.path.exists(db):  # check if old
            if self.db_backup: self.db_do_backup(db)  # do backup
            os.remove(db)  # remove

        # create the engine
        engine = create_engine('sqlite:///{}'.format(db))
        # save dataframe
        df.to_sql(table, engine, *args, **kwargs)
        log("Saved Dataframe in {}".format(db))
        return db

    def get_df_TableMain(self):
        """get the main table"""
        return self.db_sql_to_df(table=self.db_table_names['main'])

    def set_df_TableMain(self,df, db=None):
        """Save df to Table Main"""
        self.db_df_to_sql(df=df, db=db, table=self.db_table_names['main'])

    def get_df_TableKeywords(self):
        """get the keywords table"""
        return self.db_sql_to_df(table=self.db_table_names['keywords'])

if __name__ == '__main__':
    DBAPI=simpleAPI()
    print("DBAPI.get_columns()",DBAPI.get_columns())
    print("DBAPI.get_header_formated()", DBAPI.get_header_formated())
    print("DBAPI.get_table_convert()")
    print(DBAPI.get_table_convert())