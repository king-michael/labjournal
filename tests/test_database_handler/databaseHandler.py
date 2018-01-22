from databaseModel import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///./test.db', echo=False) #  if we want spam

# Establishing a session
Session = sessionmaker(bind=engine)
session = Session()


def setup_database():
    """function to create the database"""
    # create Tables
    Base.metadata.create_all(engine)

def create_SimulationEntry(simid, mediawiki=None, path=None, keywords=None):
    # type: (str, str, str, dict) -> None
    '''Wrapper around to create a SimulationEntry
    :param simid: Simulation / Labjournal ID [required]
    :param mediawiki: MediaWiki Site (\wo URL)
    :param path: Path to the files
    :param keywords: keywords / tags can be added as dict (tag: value=None)
    '''
    if keywords is None:
        sim = Simulation(
            simid=simid,
            mediawiki=mediawiki,
            path=path,
        )
    else:
        sim = Simulation(
            simid=simid,
            mediawiki=mediawiki,
            path=path,
            keywords=[Keywords(name=k,value=v) for k,v in keywords.iteritems()]
        )
    session.add(sim)


def debug_print_sims():
    """DEBUG: print simulations"""
    print 'Simulations:'
    for sim in session.query(Simulation).order_by(Simulation.simid).all():
        print "-"*50
        print ' SIM: {} - {}'.format(sim.id, sim.simid)
        for key in sim.keywords.all():
            print '  - key: {} : {}'.format(key.name, key.value)
        print '  Parents:'
        for p in sim.parents: # Association object
            psim = p.parent  # Sim object
            print '   SIM: {} - {}'.format(psim.id, psim.simid)
        print '  Children:'
        for c in sim.children:
            csim = c.child
            print '   SIM: {} - {}'.format(csim.id, csim.simid)
        print "-" * 50
        # print sim.parents
        # print sim.children