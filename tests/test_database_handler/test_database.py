from database import *

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




sim = Simulation(
    simid='MK0001',
    mediawiki='MK0001',
    path='/home/micha/somewhere'
)

session.add(sim) # add the entry to the session
sim = Simulation(
    simid='MK0002',
    mediawiki='MK0002',
    path='/home/micha/somewhereelse'
)
session.add(sim)  # add the entry to the session

session.commit() # commit the session

print "\nShow sims\n"+80*"="
sims = session.query(Simulation).all()
for sim in sims:
    print sim
    print """        id: {}
    simid: {}
    mediawiki: {}
    path: {}
    updated_on: {}""".format(sim.id, sim.simid, sim.mediawiki, sim.path, sim.updated_on)


key1 = Keywords(
    main_id = 1,
    name = "forcefield",
    value = "CHARMM"
)
key2 = Keywords(
    main_id=2,
    name="headache",
    value=None
)
key3 = Keywords(
    main_id=2,
    name="forcefield",
    value="GROMACS"
)
session.bulk_save_objects([key1,key2, key3]) # add several items in one action
session.commit()  # commit the session

print "\nShow keys\n"+80*"="
keys = session.query(Keywords).all()
for key in keys:
    print key

print "\nShow sims.keywords (One -> Many)\n" + 80 * "="
sims = session.query(Simulation).all()
for sim in sims:
    print sim
    keywords = sim.keywords.all()
    for key in keywords:
        print(key)

print "\nSelective queries\n" + 80 * "="
rv = session.query(Simulation).filter_by(simid="MK0002").one()
print '\nsession.query(Simulation).filter_by(simid="MK0002").one()'
print "=>", rv
print "rv.keywords.all()\n=>", rv.keywords.all()
print "rv.keywords.filter_by(name='headache').one()\n=>", rv.keywords.filter_by(name='headache').one()

rv = session.query(Simulation).filter(Simulation.simid=="MK0002").all()
print '\nsession.query(Simulation).filter(Simulation.simid=="MK0002").all()'
print "=>", rv

rv = session.query(Simulation).filter(Simulation.simid == "MK0002").one()
print '\nsession.query(Simulation).filter(Simulation.simid=="MK0002").one()'
print "=>", rv
print "rv.keywords.filter(Keywords.value.is_(None)).all()"
print "=>", rv.keywords.filter(Keywords.value.is_(None)).all()
print "from sqlalchemy import not_"
from sqlalchemy import not_
print "rv.keywords.filter( not_( Keywords.value.is_(None) ) ).all()"
print "=>", rv.keywords.filter( not_( Keywords.value.is_(None) ) ).all()

rv = session.query(Keywords.name,Keywords.value).select_from(Keywords)
print '\nrv = session.query(Keywords.name,Keywords.value).select_from(Keywords)'
print "rv.join(Simulation).filter(Simulation.simid == 'MK0002').all()"
print "=>", rv.join(Simulation).filter(Simulation.simid == 'MK0002').all()

print 80 * "="
rv = session.query(Simulation).all()
for i in rv:
    print i.simid,i.keywords.all()

print 80 * "="
sim = session.query(Simulation).filter(Simulation.simid == "MK0002").one()
print "original"
for key in sim.keywords.all(): print key
print "appended:"
sim.keywords.append(
    Keywords(
        main_id=sim.simid,
        name="NEW",
        value="Awesome"
    )
)

for key in sim.keywords.all(): print key
print "removed:"
sim.keywords.remove(
    sim.keywords.filter(Keywords.name == 'headache').one()
)

for key in sim.keywords.all(): print key
session.commit()

print 80 * "="
