from __future__ import absolute_import
from simdb.databaseModel import *
from sqlalchemy.orm import lazyload, subqueryload, joinedload, joinedload_all, dynamic_loader,selectinload, noload

db_path = 'micha_raw.db'


engine = create_engine('sqlite:///{}'.format(db_path))
Session = sessionmaker(bind=engine)
session = Session()



print("#"*40+'\n# normal query')
sim = session.query(Main).first()
print(sim)
print(sim.keywords)
print(sim.keywords_query.filter(Keywords.name == 'OpenMM').all())
print(sim.parents)
print(sim.parents_query.all())
print(sim.children)
print(sim.children_query.all())


# FIX ME
print("#"*40+'\n# options(noload(Main.keywords))')
sim = session.query(Main).options(noload(Main.keywords)).first()
print(sim)
print(sim.keywords)
print(sim.keywords_query.filter(Keywords.name == 'OpenMM').all())
print(sim.parents)
print(sim.parents_query.all())
print(sim.children)
print(sim.children_query.all())



#=====================================================================================#
print("+"*80)
print("Query all but order by entry_id")
sims = session.query(Main).order_by(Main.entry_id).limit(100)
for i, sim in enumerate(sims):
    print(sim)


#=====================================================================================#
print("+"*80)
print("Query only real parents")
sims = session.query(Main).join().filter(~Main.parents.any()).all()
assert any([False if len(sim.parents) != 0 else True for sim in sims]), "some one has a parent"
for sim in sims:
    if len(sim.children) > 0:
        print(sim)
        for child in sorted(sim.children, key=lambda x: x.child.entry_id):
            print(child.child)
        break


#=====================================================================================#
print("+"*80)
print("Query only one real parent")
sim = session.query(Main).join().filter(~Main.parents.any()).first()
print(sim)
header = ['entry_id', 'path', 'keywords', 'description', 'type']
print('header\n: ', header)
print([getattr(sim, attr) for attr in header])

session.close()