#/usr/bin/env python
"""
The default settings
"""

default_settings={  # Default settings

    'Database' : {  # Default settings for the database

        'db': 'tmp.db',  # Database to use
        'db_backup': True,  # should i backup the database.db
        'db_table_names': {  # names for tables
            'main'      : 'main',      # main table
            'keywords'  : 'keywords',  # keywords table
        }, # names for tables

        'formated_data' : {  # settings for formated data
            'ignore_headers': ['moddate'],  # headers to be ignored when loaded as formated data
            'convert': {  # columns to be converted
                'moddate': ['unix', 'date']  # input output
            },  # columns to be converted
        },  # settings for formated data

    },  # Default settings for the database

}  # default settings
