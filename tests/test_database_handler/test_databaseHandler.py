from databaseHandler import *

import os
try:
    os.system('rm ./test.db')
except:
    pass

db = Database(engine='sqlite:///./test.db') # , verbose=True
db.setup_database() # create the table