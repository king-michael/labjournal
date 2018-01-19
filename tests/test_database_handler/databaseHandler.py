from database import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self,
                 engine='sqlite:///:memory:',
                 verbose=False):
        """
        Class that Handles the Database
        :param engine: database to connect with e.g.: ['sqlite:///./test.db', 'sqlite:///:memory:' (default)]
        :param verbose: [False (default)]
        """

        engine_echo=True if verbose else False
        self.engine = create_engine(engine, echo=engine_echo)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def setup_database(self):
        # create Tables
        Base.metadata.create_all(self.engine)
