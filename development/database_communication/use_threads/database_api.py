from time import sleep

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread
from simdb import databaseAPI as dbapi

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
        self.sesssion = dbapi.connect_database(self.db_path)

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
        details = dbapi.get_entry_details(session=self.sesssion, entry_id=entry_id)
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
        keywords = dbapi.get_keywords(session=self.sesssion,
                                      entry_id=entry_id)
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
        df = dbapi.get_entry_table(session=self.sesssion,
                                   columns=columns)
        print(db_lock)
        db_lock.unlock()
        print(db_lock)
        return df

    def deleteLater(self):
        """
        deconstructor
        """

        self.sesssion.close()


class DatabaseThread(QThread):
    def __init__(self, db_path, parent=None):
        super(QThread, self).__init__(parent)
        self.db_path = db_path
    def run(self):
        self.database = Database(db_path=self.db_path)
        self.running = True
        while self.running:
            sleep(0.25)

    def __del__(self):
        self.exiting = True
        self.wait()

if __name__ == '__main__':
    db_path = 'example_simulations.db'
    ID = 'MK0085'

    import sys
    from PyQt5.QtWidgets import QWidget, QPushButton
    from PyQt5 import QtCore, QtWidgets

    class test_main_thread(QWidget):
        def __init__(self):
            super(self.__class__, self).__init__()

            layout = QtWidgets.QHBoxLayout()

            btn = QtWidgets.QPushButton("get data")
            btn.clicked.connect(self.get_data)
            layout.addWidget(btn)

            self.setLayout(layout)

            self.databaseThread = DatabaseThread(db_path=db_path)
            self.databaseThread.start()

        def get_data(self):
            print(self.databaseThread.database.get_entry_details(entry_id=ID))


    app = QtWidgets.QApplication(sys.argv)
    window = test_main_thread()
    window.show()
    sys.exit(app.exec_())
