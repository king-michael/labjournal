
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

    keywords = relationship('Keywords', backref='simid', lazy='dynamic')

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
        main_id = sim.id,
        name = "forcefield",
        value = "CHARMM"
    )
    key2 = Keywords(
        main_id=sim.id,
        name="forcefield",
        value=None
    )

    session.bulk_save_objects([key1,key2]) # add several items in one action
    session.commit()  # commit the session

    print "\nShow keys\n"+80*"="
    keys = session.query(Keywords).all()
    for key in keys:
        print key

    print "\nShow sims.keywords\n" + 80 * "="
    sims = session.query(Simulation).all()

    for sim in sims:
        print sim.keywords
        keywords = session.query(sim.keywords).all()
        print "TEST"
        for key in keywords:
            print(key)