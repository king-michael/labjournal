
#from database import *
import os
try:
    os.system('rm ./test.db')
    print('deleted ./test.db')
except:
    pass

import databaseHandler as db
from databaseModel import *

db.setup_database()

sim1 = Simulation(
    simid='MK0001',
    mediawiki='MK0001',
    path='dasd'
)

sim2 = Simulation(
    simid='MK0002',
    mediawiki='MK0002',
    path='dasf',
    # keywords=[Keywords(name='key1',value="bla"),Keywords(name="key2",value="blub")],

)

sim3 = Simulation(
    simid='MK0003',
    mediawiki='MK0003',
    path='dasd'
)

sim4 = Simulation(
    simid='MK0004',
    mediawiki='MK0004',
    path='dasd'
)

sim5 = Simulation(
    simid='MK0005',
    mediawiki='MK0005',
    path='dasd'
)

aso1 = Association(
    parent=sim1,
    child=sim2
)

aso2 = Association(
    parent=sim1,
    child=sim3
)

aso3 = Association(
    parent=sim2,
    child=sim4
)

aso4 = Association(
    parent=sim4,
    child=sim1
)

aso5 = Association(
    parent=sim3,
    child=sim4
)



db.session.add(sim1)
db.session.add(sim2)
db.session.add(sim3)
# print sim3.id
db.session.add(sim4)
db.session.add(sim5)
# print sim4.id
# db.session.commit()
# print sim3.id
# print sim4.id

sim4.children.append(Association(child=sim5))
sim4.children.append(Association(child=sim4))
# sim4.children.append(sim5)

db.session.add(aso1)
db.session.add(aso2)
db.session.add(aso3)
db.session.add(aso4)
db.session.add(aso5)

# db.create_SimulationEntry(
#     simid='MK0001',
#     mediawiki='MK0001',
#     path='dasd'
# ) # create an entry
#
# db.create_SimulationEntry(
#     simid='MK0002'
# ) # create an entry
#
# db.create_SimulationEntry(
#     simid='MK0003',
#     keywords={'tag01':None,'keyword01':'STRING','keyword02':1}
# ) # create an entry
#
# db.create_SimulationEntry(
#     simid='MK0004',
#     keywords={'tag01':None,'linker':'k48','bla':"blub"}
# ) # create an entry



db.session.commit()  # commit the session
db.debug_print_sims()

sim4 = db.session.query(Simulation).filter(Simulation.simid == "MK0004").one()
print "IM NOT A ZWITTER!"
sim4.children.remove(sim4.children.filter_by(child=sim4).one())
db.session.commit()  # commit the session
db.debug_print_sims()
# q = db.session.query(Association).filter(Association.parent_id==1)
# rv = q.one()
# print rv
# print rv.parent
# print rv.child