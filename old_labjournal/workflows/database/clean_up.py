"""Cleanup for the database"""

from old_labjournal.core.databaseModel import *

session = establish_session('sqlite:///examples/test_WORKS.db')
for sim in session.query(Main).all():
    list_keywords = [keyword for keyword in sim.keywords.all()]
    keys = [k.name for k in list_keywords]
    for k in list(set(keys)):
        if keys.count(k) > 1:
            for i,keyword in enumerate(sim.keywords.filter(Keywords.name == k).all()):
                if i>0:
                    session.delete(keyword)
session.commit()
session.delete()