"""
Test the fileFinder
"""

import logging
logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

import sys
sys.path.append("../../..")

from utils.fileFinder import *
from core.databaseModel import *


fileFinder = FileFinder(
    pattern='_info_',
    path='/home/micha/SIM-PhD-King',
    dir_ignore=['OLD', 'old', 'Old', 'TMP', 'tmp', 'rm', 'templates', 'testcase'])

SIM_IDS=[]
PATHS=[]
DATAS=[]

logger.info('create_database:create_database: FIND FILES')
ERRORS=False
WARNINGS=False
for fname in fileFinder.find_files():
    data = fileHandler.get_data_from_file(fname)
    data['path']=os.path.dirname(fname)

    try:
        SIM_IDS.append(data['ID']) # throws an ERROR if ID not in data
    except:
        print "ERROR: ID:\n ", fname # shows the FILE if an error is thrown
        ERRORS = True

    try:
        data['MEDIAWIKI']  # throws an ERROR if MEDIAWIKI not in data
    except:
        print "WARNING: NO MEDIAWIKI ENTRY:\n ", fname
        WARNINGS = True

    DATAS.append(data)  # only append if the first two cases are passed
    PATHS.append(fname)  # only append if the first two cases are passed

if ERRORS:
    exit()
if WARNINGS:
    exit()

logger.info('create_database:create_database: CHECK FOR DUPLICATES IN sim_id')

from collections import Counter
sim_count=Counter(SIM_IDS)
DUPLICATES=False
for k,v in sim_count.iteritems():
    if v != 1:
        DUPLICATES=True
        print "#======================================================#"
        for sim, path in zip(SIM_IDS,PATHS):
            if k == sim:
                print sim,path
if DUPLICATES:
    exit()

logger.info('create_database:create_database: Create the Database')
db = 'micha_raw.db'
try:
    os.remove(db)
    logger.info('create_database:create_database: removed old file: %s', db)
except:
    pass
engine = create_engine(db_address, echo=False) #  if we want spam
# Establishing a session
Session = sessionmaker(bind=engine)
session = Session()
setup_database(engine)
for data in DATAS:
    sim = Simulation(
       sim_id=data['ID'],
       mediawiki=data['MEDIAWIKI'],
       path=data['path'],
       description=data['INFO'] if 'INFO' in data.keys() else None
    )
    session.add(sim)
session.commit()
session.close()
logger.info('create_database:create_database: Created the database: %s', db)