#BEGIN IMPORT SYSTEM
from __future__ import print_function
import datetime
from shutil import copy2
# Database:
import pandas as pd
from sqlalchemy import create_engine
#END IMPORT SYSTEM


#BEGIN IMPORT MINE
from logger import * # get all utils
from utils import *
from filefinder import *
#END IMPORT MINE

log=Logger()

class simpleAPI(object):
    """Simple API for the Database"""
    def __init__(self):
        self.DatabaseIndex = DatabaseIndex()
        self.load_sql()
        self.settings = {
            'ignore_headers': ['realpath'],
            'convert': {
                'moddate': ['unix', 'date']  # input output
            },
        }

    def load_sql(self):
        self.df = self.DatabaseIndex.db_sql_to_df()

    def get_columns(self):
        '''get Columns of Dataframe'''
        return list(self.df.columns)  # [str(i) for i in self.df.columns]

    def get_header_formated(self):
        '''get the Header in formated form'''
        header = self.get_columns()
        for i in self.settings['ignore_headers']: header.remove(i)
        return header

    def get_table_raw(self):
        return self.df.values

    def get_table(self, inp=None):
        '''get table of Dataframe'''
        if inp is None:
            return self.df.values
        elif type(inp) == type(str()):
            return self.df.loc[:, inp].values
        elif type(inp) == type(int()):
            return self.df.iloc[:, inp].values
        elif type(inp) == type(list([])):
            if type(inp[0]) == type(int()):
                return self.df.iloc[:, inp].values
            else:
                return self.df.loc[:, inp].values
        raise TypeError('Could not use dtype of get_table(inp):\n ' + str(type(inp)))

    def get_table_convert(self):
        """Returns the table in converted form (without ignore_headers)
        :return: df.values
        """
        header = self.get_header_formated()
        df = self.df.loc[:, header]

        def transform_date(x):
            return datetime.datetime.fromtimestamp(float(x)).strftime("%Y/%m/%d")

        for i in self.settings['convert']:
            if i == 'moddate':
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

        def transform_date(x):
            return datetime.datetime.fromtimestamp(float(x)).strftime("%Y/%m/%d")

        for i in self.settings['convert']:
            if i == 'moddate':
                df[i] = transform_date(df[i])

        return header, df.values

class DatabaseIndex():
    def __init__(self,**kwargs):
        '''Class to manage the Index Database'''
        
        self.defaults={
            'db'                 :  'tmp.db', # Database to use
            'db_backup'          :  True, # should i backup the database.db
            'keys'               :  ['id_db'], # ID field
            'db_table_names'    :  { # names for tables
                                    'DataIndex' : 'DataIndex', # DataIndex table
                                    }
        }
        self.init_kwargs(**self.defaults) # set defaults
        self.init_kwargs(**kwargs) # set kwargs
        
    def init_kwargs(self,**kwargs):
        '''set kwargs'''
        
        self.kwargs = kwargs
        for k,v in kwargs.iteritems(): setattr(self,k,v)
            
    def db_do_backup(self,db,db_back=None):
        '''backup a Database'''
        
        
        if db_back is None: db_back=db+".bck"
        copy2(db,db_back) # shutil.copy2(src,dst)
        
            
    def convert_array2dict(self,array,keys=None):
        '''
        convert array (list of list) to dict
        keys=dict.keys = array collumn
        return dict
        '''
        
        if keys is None: keys=range(len(array[0])) # if key not set
        # init dict
        result=dict((i,[]) for i in keys)
        for entry in array:
            for v,key in zip(entry,keys):
                result[key]+=[v]
        return result
            
    def db_create_dataframe(self,*args,**kwargs):
        '''Create a new Pandata Dataframe'''
        # argument handler
        list_args=['dataset','keys']
        kwargs=dict(subdict(self.__dict__,list_args),**kwargs)
        for i,arg in enumerate(args):
            kwargs.update({list_args[i]:arg})
        # setup dataframe
        df = pd.DataFrame(self.convert_array2dict(kwargs['dataset'],kwargs['keys']))
        return df
    
    def db_df_to_sql(self,df=None,db=None,table=None,*args,**kwargs):
        '''Saves Dataframe as SQL data'''
        
        if db is None: db=self.db
        if table is None: table=self.db_table_names['DataIndex']
        if df is None: 
            if hasattr(self,'df'): 
                df=self.df 
            else:
                raise StandardError("Cant save dataframe without a dataframe defined")
        defaults={'if_exists' : 'replace'}
        kwargs=dict(defaults,**kwargs)
        
        # Create new file
        if os.path.exists(db): # check if old
            if self.db_backup: self.db_do_backup(db) # do backup
            os.remove(db) # remove

        # create the engine    
        engine = create_engine('sqlite:///{}'.format(db))
        # save dataframe        
        df.to_sql(table,engine,*args,**kwargs)
        log("Saved Dataframe in {}".format(db))
        return db
    
    def db_sql_to_df(self,db=None, table=None):
        '''Loads in Database from SQL'''
        if db is None: db=self.db
        if table is None: table=self.db_table_names['DataIndex']
        # create the engine
        engine = create_engine('sqlite:///{}'.format(db))
        #FIXME ?? read_sql or read_sql_table ??
        df = pd.read_sql_table(table,engine,index_col='index')
        log("Loaded Dataframe from {}".format(db))
        return df
    
if __name__ == '__main__':
    #t=FileFinder()
    #files=t()
    #dataset, keys = t.build_dataset(files)
    #dataset, keys = t.dataset_init(files=[])

    ## if __name__ == '__main__':
    #dbindex = DatabaseIndex()
    #dbindex.db_create(dataset=dataset, keys=keys)
    #df = dbindex.db_create_dataframe(dataset,keys)
    #dbindex.db_df_to_sql(df)

    DBAPI=simpleAPI()
