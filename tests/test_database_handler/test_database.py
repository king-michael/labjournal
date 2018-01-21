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
print "#Add Simulation with new keywords in one"+"\n"+40*"-"

sim = Simulation(
    simid='MK0003',
    mediawiki='MK0003',
    path='/home/micha/somewhereelse',
    keywords=[
        Keywords(name='test'),
        Keywords(name='forcefield', value='AMBER')
    ]
)

session.add(sim)  # add the entry to the session
session.commit() # commit the session

print 'Simulations:'
for sim in session.query(Simulation).all():
    print ' SIM: {} - {}'.format(sim.id,sim.simid)
    for key in sim.keywords.all():
        print '  - key: {} : {}'.format(key.name,key.value)

print 'Keywords:'
rv = session.query(Simulation.simid,Keywords.name,Keywords.value).select_from(Keywords,Simulation)
rv = rv.filter(Simulation.id == Keywords.main_id)
for key in rv.all():
    print(key)


############################################################################################
# Pandas
############################################################################################
print '\n\n\n'
print '#' * 80
print '# PANDAS STUFF'
print '#' * 80

print 'Use pandas to load the entrys:'
import pandas as pd
#################################################################
print '='*80
print 'get Simulation.__tablename__ : {}'.format(Simulation.__tablename__)
print '='*80
df = pd.read_sql_table(Simulation.__tablename__,engine,index_col='id')  # get the dataframe
print 'df:\n', df

#################################################################
print '='*80
print "get columns=['simid', 'mediawiki', 'path']"
print '='*80
df = pd.read_sql_table(Simulation.__tablename__,
                        engine,
                        columns=['simid', 'mediawiki', 'path'] ,
                        index_col='id')  # get the dataframe
print 'df:\n', df

#################################################################
print '='*80
print 'get Keywords.__tablename__ : {}'.format(Keywords.__tablename__)
print '='*80
df = pd.read_sql_table(Keywords.__tablename__,engine,index_col='id')  # get the dataframe
print 'df:\n', df

#################################################################
print '='*80
print 'get dataframe with keywords + value'.format(Keywords.__tablename__)
print '='*80

query = session.query(Keywords).filter(not_(Keywords.value.is_(None)))
df = pd.read_sql_query(str(query),engine, 'keywords_id')
print df
print 'SQLAlchemy results:'
for i in query.all(): print ' ',i

############################################################################################
# Usefull stuff
############################################################################################
print '#'*80 + '\n# Usefull stuff\n' , '#'*80

#################################################################
print '='*80 , '\nget unqiue keywords\n' + '='*80

from sqlalchemy import distinct
query = session.query(distinct(Keywords.name)).select_from(Keywords)\
    .filter(not_(Keywords.value.is_(None)))
print query.all()

#################################################################
print '='*80 , '\nget unqiue tags\n' , '='*80

from sqlalchemy import distinct
query = session.query(distinct(Keywords.name)).select_from(Keywords)\
    .filter(Keywords.value.is_(None))
print query.all()