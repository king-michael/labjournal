from __future__ import print_function, absolute_import
import sys

from database_api import Database


db_path = 'micha_raw.db'
ID = 'MK0200'

database = Database(db_path=db_path)
details = database.get_entry_details(entry_id=ID)
keywords = database.get_entry_keywords(entry_id=ID)
print(details)
print(keywords)

