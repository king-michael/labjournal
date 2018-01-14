from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String

Base = declarative_base()

class Simulation(Base):
    __tablename__ = 'main'

    id = Column(Integer, primary_key=True)
    simid =  Column(String(50), index=True, unique=True) # should be discussed
    mediawiki = Column(String(255))
    path = Column(String(255))

    def __repr__(self):
        return """{}(simid='{}',
    mediawiki='{}',
    path='{}' )""".format(self.__class__.__name__,self.simid,self.mediawiki,self.path)

# Connecting to an engine
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True) #  if we want spam
#engine = create_engine('sqlite:///./test.db') #  if we want spam

# Establishing a session
from sqlalchemy.orm import sessionmaker

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
    session.commit() # commit the session

    sims = session.query(Simulation).all()
    for sim in sims:
        print(sim)