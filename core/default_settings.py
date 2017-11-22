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

    'mediawiki' : {  # MediaWiki settings
        'prefix'  : "http://134.34.112.156:777/mediawiki/index.php/",  # prefix
        'browser' : 'browser',  # how to open it [browser = defaultbrowser]
    },  # MediaWiki settings

    'LAMMPS' : {  # Settings for LAMMPS

        'folders' : {  # Folders
            'production'            : 'production',            # folder where the production run is
            'EM_and_Equilibration'  : 'EM_and_Equilibration',  # folder where the EM and Equilibration is
            'analysis'              : 'analysis',              # folder where the normal analysis will be saved
            'older_analysis_MetaD'  : 'analysis_MetaD',        # folder where MetaDynamic analysis will be saved
        },  # folders

        'pattern' : {
            'trajectory'    : 'trajectory..*.dcd',  # trajectory file with .* = run_no
            'logfile'       : 'log..*.lammps',      # log file with .* = run_no
            'final_data'    : 'final_data..*',      # final data file with .* = run_no
            'final_restart' : 'final_restart..*',   # final restart file with .* = run_no
        },  # pattern

        'thermo' : {
            'xlabel'            : 'Step',  # xlabel for thermo data (possible also 'Time' but risky not work for everything)
            'list_keywords'     : ['PotEng', 'Temp', 'Press', 'Volume'],  # list of keywords to use for analysis
            'BUFFER_READ'       : 200,  # readin buffer to check for keywords (number of chars in the Step KEYWORDS line)
            'save_subfolder'    : 'plot_log' # subfolder to save extracted data in
        },
        'plot' : {
            'xlabel' : 'Step'
        },
    },  # LAMMPS
}  # default settings
