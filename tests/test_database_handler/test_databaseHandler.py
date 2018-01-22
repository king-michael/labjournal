
#from database import *
import os
try:
    os.system('rm ./test.db')
    print('deleted ./test.db')
except:
    pass

import databaseHandler as db

db.setup_database()

db.create_SimulationEntry(
    simid='MK0001',
    mediawiki='MK0001',
    path='dasd'
) # create an entry

db.create_SimulationEntry(
    simid='MK0002'
) # create an entry

db.create_SimulationEntry(
    simid='MK0003',
    keywords={'tag01':None,'keyword01':'STRING','keyword02':1}
) # create an entry

db.session.commit()  # commit the session
db.debug_print_sims()
