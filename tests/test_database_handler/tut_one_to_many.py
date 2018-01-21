"""
Tutorial around many-to-many relationships

Tutorial:
  Creating Many-To-Many Relationships in Flask-SQLAlchemy
  https://www.youtube.com/watch?v=OvhoYbjtiKc
more info at:
  http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-many-to-many-relationship
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker




# Base class
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    pets = relationship('Pet', backref='owner', lazy='dynamic')

class Pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    owner_id = Column(Integer(), ForeignKey('person.id'))


if __name__ == '__main__':
    import os

    try:
        os.system("rm ./tut_one_to_many.db")
    except:
        pass
    engine = create_engine('sqlite:///./tut_one_to_many.db')  # if we want  to inspect it
    #engine = create_engine('sqlite:///:memory:', echo=False) #  if we want spam set echo=True
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print 'add Persons'
    person1 = Person(name='Anthony')
    person2 = Person(name='Cindy')
    session.add(person1)
    session.add(person2)
    session.commit()

    print 'Add pets'
    pet1 = Pet(name='Spot', owner=person1)
    session.add(pet1)
    session.commit()

    pet2 = Pet(name='Simba', owner=person1)
    pet3 = Pet(name='Sylverster', owner=person2)
    pet4 = Pet(name='MR. Frizzels', owner=person2)
    session.add(pet2)
    session.add(pet3)
    session.add(pet4)
    session.commit()

    print 'Queries'

    print "session.query(Person).filter_by(name='Anthony').first()"
    r = session.query(Person).filter_by(name='Anthony').first()
    print r
    print r.pets
    print r.pets.all()
    for i in r.pets.all():
        print(i.name)

    print 'session.query(Pet).filter_by(owner_id=2).all()'
    rv = session.query(Pet).filter_by(owner_id=2).all()
    for i in rv:
        print(i.name)