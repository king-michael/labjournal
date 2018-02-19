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
print "FIND FILES"
for fname in fileFinder.find_files():
    data = fileHandler.get_data_from_file(fname)
    data['path']=os.path.dirname(fname)
    try:
        SIM_IDS.append(data['ID'])
        data['MEDIAWIKI']
        DATAS.append(data)
        PATHS.append(fname)
    except:
        print fname
        print data


print "CHECK FOR DUPLICATES IN sim_id"
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
print "Create the Database"
db = 'test_micha.db'
try:
    os.remove(db)
except:
    pass
engine, session = establish_session('sqlite:///{}'.format(db))
#engine, session = establish_session()
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