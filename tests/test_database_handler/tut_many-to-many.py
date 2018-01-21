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

subs = Table('subs', Base.metadata,
             Column('user_id',Integer(), ForeignKey('user.user_id')),
             Column('channel_id', Integer(), ForeignKey('channel.channel_id'))
)

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True)
    name = Column(String(20))
    subscriptions = relationship('Channel',
                                 secondary=subs,
                                 backref=backref('subscribers',
                                                 lazy='dynamic'), # add subscribers to Channel model
                                 )
class Channel(Base):
    __tablename__ = 'channel'
    channel_id = Column(Integer(), primary_key=True)
    channel_name = Column(String(20))



if __name__ == '__main__':
    import os

    try:
        os.system("rm ./tut_many_to_many.db")
    except:
        pass
    #engine = create_engine('sqlite:///./tut_many_to_many.db')  # if we want  to inspect it
    engine = create_engine('sqlite:///:memory:', echo=False) #  if we want spam set echo=True

    Session = sessionmaker(bind=engine)
    session = Session()

    # create Tables
    Base.metadata.create_all(engine)
    user1 = User(name='Anthony')
    user2 = User(name='Stacy')
    user3 = User(name='George')
    user4 = User(name='Amber')

    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.commit()
    print 'user.user_id, user.name'
    for user in session.query(User).all():
        print user.user_id, user.name

    channel1 = Channel(channel_name='Pretty Printed')
    channel2 = Channel(channel_name='Cat Videos')
    session.add(channel1)
    session.add(channel2)
    session.commit()
    print 'channel.channel_id, channel.channel_name'
    for channel in session.query(Channel).all():
        print channel.channel_id, channel.channel_name

    channel1.subscribers.append(user1)
    session.commit()
    channel1.subscribers.append(user3)
    channel1.subscribers.append(user4)
    channel2.subscribers.append(user2)
    channel2.subscribers.append(user4)
    session.commit()

    print 'sub.user_id, sub.channel_id'
    for sub in session.query(subs).all():
        print sub.user_id, sub.channel_id