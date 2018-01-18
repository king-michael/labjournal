
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

# Base class
Base = declarative_base()

#===================================================================#
# Database Models
#===================================================================#
# Column parameters:
#  http://docs.sqlalchemy.org/en/latest/core/metadata.html?highlight=onupdate#sqlalchemy.schema.Column.params.onupdate


class Simulation(Base):
    __tablename__ = 'main'

    id = Column(Integer(), primary_key=True)
    simid =  Column(String(50), unique=True) # should be discussed
    mediawiki = Column(String(255))
    path = Column(String(255))
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    keywords = relationship('Keywords', backref='simid' , lazy='dynamic')  # lazy='dynamic' -> returns query so we can filter
    def __repr__(self):
        return """{}(simid='{}', mediawiki='{}', path='{}')""".format(
            self.__class__.__name__,
            self.simid,
            self.mediawiki,
            self.path)

class Keywords(Base):
    __tablename__ = 'keywords'

    id = Column(Integer(), primary_key=True)
    main_id =  Column(Integer(), ForeignKey('main.id')) # , index=True
    name  =  Column(String(255))
    value =  Column(String(255), nullable=True)

    #simid = relationship("Simulation", backref('keywords'))

    def __repr__(self):
        return "{}(simid='{}', name='{}', value='{}')".format(
            self.__class__.__name__,
            self.main_id,
            self.name,
            self.value)



# Connecting to an engine
#engine = create_engine('sqlite:///:memory:', echo=False) #  if we want spam
import os
os.system("rm ./test.db")
engine = create_engine('sqlite:///./test.db') #  if we want spam

# Establishing a session


Session = sessionmaker(bind=engine)
session = Session()

# create Tables
Base.metadata.create_all(engine)



if __name__ == '__main__':

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

    from sqlalchemy.orm import load_only
    rv = session.query(Keywords.name,Keywords.value).select_from(Keywords)
    print '\nrv = session.query(Keywords.name,Keywords.value).select_from(Keywords)'
    print "rv.join(Simulation).filter(Simulation.simid == 'MK0002').all()"
    print "=>", rv.join(Simulation).filter(Simulation.simid == 'MK0002').all()

    # SELECT keywords.name FROM keywords
    # JOIN main ON keywords.main_id = main.id
    # WHERE main.simid = 'MK0002'