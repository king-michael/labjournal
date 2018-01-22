from databaseModel import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
try:
    os.system('rm ./test.db')
except:
    pass
engine = create_engine('sqlite:///./test.db', echo=False) #  if we want spam
#engine = create_engine('sqlite:///:memory:', echo=False) #  if we want spam

# Establishing a session
Session = sessionmaker(bind=engine)
session = Session()

# create Tables
Base.metadata.create_all(engine)


sim1 = Simulation(simid='MK0001')
sim2 = Simulation(simid='MK0002')
sim3 = Simulation(simid='MK0003')
sim4 = Simulation(simid='MK0004')
session.add(sim1)  # add the entry to the session
session.add(sim2)  # add the entry to the session
session.add(sim3)  # add the entry to the session
session.add(sim4)  # add the entry to the session

session.commit() # commit the session

rel1 = Association(
    parent_id=2,
    child_id=1
)
session.add(rel1)
rel2 = Association(
    parent_id=2,
    child_id=3
)
session.add(rel2)
session.commit()


#sim1.children.append(sim4)

for rv in session.query(Simulation).all():
    print rv
    print 'parents', rv.parents
    print 'children', rv.children


print '='*80
print 'Association table'
for rv in session.query(Association).all():
    print rv
    print ' .parent:', rv.parent
    print ' .child:', rv.child

rv = session.query(Simulation).filter(Simulation.simid=='MK0002').one()
print rv
print rv.children
rv.children.remove(rel1)
print rv.children