from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from simdb import databaseAPI as dbapi
from simdb import databaseModel as db


db_lock = QtCore.QReadWriteLock()
"""lock for the database access"""


class Database(QObject):

    def __init__(self, db_path, parent=None):
        """
        Database object (to live on another thread) to access the database.

        Parameters
        ----------
        db_path : str
            Path to the database
        parent : QObject or None
            Parent
        """
        super(QObject, self).__init__(parent)
        print(db_path)
        self.db_path = db_path

    def get_entry_details(self, entry_id):
        """
        Get entry details for an entry. (without keywords etc)

        Parameters
        ----------
        entry_id : str
            entry_id in the database

        Returns
        -------
        details : dict
            Dictionary of entry details.
        """

        db_lock.lockForRead()
        details = dbapi.getEntryDetails(db_path=self.db_path, entry_id=entry_id)
        db_lock.unlock()

        return details

    def get_entry_keywords(self, entry_id):
        """
        Get entry keywords for an entry.

        Parameters
        ----------
        entry_id : str
            entry_id in the database

        Returns
        -------
        keywords : dict
            Dictionary of keywords for an entry.
        """

        db_lock.lockForRead()
        keywords = dbapi.getEntryKeywords(db_path=self.db_path, entry_id=entry_id)
        db_lock.unlock()

        return keywords

    def get_entry_table(self,
                        columns=["entry_id", "path", "created_on", "added_on", "updated_on", "description"],
                        load_keys=True,
                        load_tags=True):
        """

        Parameters
        ----------
        columns : List[str]
            List of columns to get from the `Main` table.
        load_keys : bool
            if keywords should also be loaded.
        load_tags : bool
            if tags should also be loaded.

        Returns
        -------
        df : pandas.Dataframe
            Pandas Dataframe from the `Main` table
        """
        print(db_lock)
        db_lock.lockForRead()
        df = dbapi.getEntryTable(db_path=self.db_path, columns=columns, load_keys=load_keys, load_tags=load_tags)
        print(db_lock)
        db_lock.unlock()
        print(db_lock)
        return df


if __name__ == '__main__':
    db_path = '../test/micha_raw.db'
    ID = 'MK0200'

    database = Database(db_path=db_path)
    details = database.get_entry_details(entry_id=ID)
    keywords = database.get_entry_keywords(entry_id=ID)
    print(details)
    print(keywords)
