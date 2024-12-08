import sys
import time
from time import sleep
from PyQt5 import QtCore, QtWidgets, QtGui

# usefull links:
# https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt

from database_api import DatabaseThread

db_path = 'example_simulations.db'
ID = 'MK0085'


class test_main_thread(QtWidgets.QWidget):
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

        print(self.databaseThread.database.get_entry_details(ID))




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = test_main_thread()
    window.show()
    sys.exit(app.exec_())