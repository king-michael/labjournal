"""
Script to find parent - child relationships based on sim_id
"""

db_raw = 'micha_add_missing.db'
db     = 'micha_add_parents.db'

warn_depth=10
import logging
logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

import sys
sys.path.append("../../..")

from labjournal.core.databaseModel import *

from shutil import copy2
logger.info('create_database:find_parents: copy %s --> %s', db_raw, db)
copy2(db_raw,db)

session = establish_session('sqlite:///{}'.format(db))

rv = session.query(Main.sim_id).all()

SIM_IDS = [sim_id[0] for sim_id in rv]
SIM_ID_MAIN = sorted(list(set([sim_id[0][:6] for sim_id in rv])))
tmp=[len(sim_id) for sim_id in SIM_IDS]
max_depth=max(tmp)
if max_depth > warn_depth:
    logger.warn('create_database:find_parents: depth to long (depth: %d ; exampleID: %s)',
                max_depth, SIM_IDS[tmp.index(max_depth)])

for sim_id in SIM_IDS:
    if   len(sim_id) == 6: # parents
        pass
    elif len(sim_id) == 8: # child
        parent = sim_id[:6]
        sim_child = session.query(Main).filter(Main.sim_id == sim_id).one()
        sim_parent = session.query(Main).filter(Main.sim_id == parent).one()
        ret = session.query(  # check if parent has grandparent
            exists().where(
                and_(
                    AssociationMainKeywords.parent == sim_parent,
                    AssociationMainKeywords.child == sim_child
                )
            )).scalar()
        if not ret: # if the releationship is not there yet
            sim_parent.children.append(AssociationMainKeywords(parent=sim_parent,
                                                               child=sim_child,
                                                               extra_data='SUB'))
            logger.info('create_database:find parents: ADDED: parent: %s child: %s',
                        sim_parent.sim_id,
                        sim_child.sim_id)
    elif len(sim_id) == 10: # grandchild
        parent = sim_id[:8]
        grandparent = sim_id[:6]
        sim_child = session.query(Main).filter(Main.sim_id == sim_id).one()
        sim_parent = session.query(Main).filter(Main.sim_id == parent).first()
        if sim_parent is None: # handle if the entry dont exist
            sim_parent = Main(
                sim_id=parent,
                mediawiki=grandparent,
                path='',
                description="--------",
            )
            session.add(sim_parent)
        ret = session.query(  # check if parent has grandparent
            exists().where(
                and_(
                    AssociationMainKeywords.parent == sim_parent,
                    AssociationMainKeywords.child == sim_child
                )
            )).scalar()
        if not ret:  # if the releationship is not there yet
            sim_parent.children.append(AssociationMainKeywords(parent=sim_parent,
                                                               child=sim_child,
                                                               extra_data='SUBSUB'))
            logger.info('create_database:find parents: ADDED: parent: %s child: %s',
                        sim_parent.sim_id,
                        sim_child.sim_id)
        sim_grandparent = session.query(Main).filter(Main.sim_id == grandparent).one()
        ret = session.query( # check if parent has grandparent
            exists().where(
                and_(
                    AssociationMainKeywords.parent == sim_grandparent,
                    AssociationMainKeywords.child == sim_parent
                )
            )).scalar()
        if not ret: # if grandchild relation is not here
            sim_grandparent.children.append(AssociationMainKeywords(parent=sim_grandparent,
                                                                    child=sim_parent,
                                                                    extra_data='SUB'))
            logger.info('create_database:find parents: ADDED: parent: %s child: %s',
                        sim_grandparent.sim_id,
                        sim_parent.sim_id)
session.commit()
session.close()
logger.info('create_database:create_database: Created the database: %s', db)