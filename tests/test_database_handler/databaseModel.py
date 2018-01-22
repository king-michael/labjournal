"""
Database Model
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy import DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from datetime import datetime
from sqlalchemy import Table
# Base class
Base = declarative_base()

#===================================================================#
# Database Models
#===================================================================#
# Column parameters:
#  http://docs.sqlalchemy.org/en/latest/core/metadata.html?highlight=onupdate#sqlalchemy.schema.Column.params.onupdate

# relationship:
#    lazy = 'dynamic'  # returns query => can be used with .filter .order => .all()
#    lazy = 'select'   # automatically runs a second query if accessed, returns results (two query in total)
#    lazy = 'joined'   # joins them at the query of the entry (one query in total)
#    lazy = 'subquery' #  same as joined, otherway, different performance


#class Association(Base):
#    __tablename__ = 'association'
#    parent_id = Column(Integer, ForeignKey('main.id'), primary_key=True)
#    child_id = Column(Integer, ForeignKey('main.id'), primary_key=True)
#    extra_data = Column(String(50))
#    parent = relationship("Simulation",foreign_keys='Association.parent_id',  back_populates="parents")
#    child = relationship("Simulation", foreign_keys='Association.child_id', back_populates="children")#
#
#    def __repr__(self):
#        return """{}(parent='{}', child='{}', extra_data='{}')""".format(self.__class__.__name__,
#                                                                         self.parent_id,
#                                                                         self.child_id,
#                                                                        self.extra_data)
#
#add to Simulation:
# children = relationship('Association',
#                            foreign_keys='Association.parent_id')
# parents = relationship('Association',
#                            foreign_keys='Association.child_id')




class Simulation(Base):
    __tablename__ = 'main'

    id = Column(Integer(), primary_key=True, index=True)
    simid =  Column(String(50), unique=True, index=True) # should be discussed
    mediawiki = Column(String(255))
    path = Column(String(255))
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    keywords = relationship('Keywords',
                            backref='simid' , # check cascade_backrefs
                            lazy='dynamic', # lazy='dynamic' -> returns query so we can filter
                            cascade="all, delete-orphan", # apply delete also for childs
                            passive_deletes=True, # apply delete also for childs
                            )  # lazy='dynamic' -> returns query so we can filter



    def __repr__(self):
        return """{}(simid='{}', mediawiki='{}', path='{}')""".format(
            self.__class__.__name__,
            self.simid,
            self.mediawiki,
            self.path)

class Keywords(Base):
    __tablename__ = 'keywords'

    id = Column(Integer(), primary_key=True, index=True)
    main_id =  Column(Integer(), ForeignKey('main.id') , index=True)
    name  =  Column(String(255), index=True)
    value =  Column(String(255), nullable=True)

    #simid = relationship("Simulation", backref('keywords'))

    def __repr__(self):
        return "{}(simid='{}', name='{}', value='{}')".format(
            self.__class__.__name__,
            self.main_id,
            self.name,
            self.value)
