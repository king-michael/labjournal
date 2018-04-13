
# generate Uitest.py
#  pyuic4 test.ui -o Uitest.py

import sys
sys.path.append("../../")
import labjournal.core.databaseModel as db

from PyQt5 import QtWidgets

from Uitest import Ui_MainWindow

class GUi_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,**kwargs):
        super(GUi_MainWindow,self).__init__(**kwargs)

        self.setupUi(self)
        self._init_menubar()

        # pushButton modify
        self.pushButton.clicked.connect(self.update_table)
        self.pushButton.setText("Connect to Database")
        # add a label
        self.label = QtWidgets.QLabel('Selected Database: {}'.format('----------'))
        self.verticalLayout.addWidget(self.label)

        #self.db = 'test_new.db'

        #self.update_table()

    def update_table(self):
        """update table"""
        if not hasattr(self,'db'):
            raise StandardError("Not connected to a database")

        if not hasattr(self,'tableWidget'):
            print "Create tableWidget"
            self.tableWidget = QtWidgets.QTableWidget()  # create a table
            self.verticalLayout.addWidget(self.tableWidget)  # add it to the layout

        session = db.establish_session('sqlite:///{}'.format(self.db))
        print "connect to database: {}".format(self.db)
        rv = session.query(db.Main).all()

        # update table
        self.tableWidget.setRowCount(0) # set rowCount back to zero
        self.tableWidget.setColumnCount(3) # set number of Columns

        for row_number, sim in enumerate(rv):
            self.tableWidget.insertRow(row_number) # insert a row
            # create row entries
            self.tableWidget.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(sim.sim_id)))
            self.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(sim.mediawiki)))
            self.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(sim.sim_type)))


    def _init_menubar(self):

        # get the menuBar
        mainMenu = self.menuBar()
        # create a entry
        fileMenu = mainMenu.addMenu('&File')
        # create an action
        extractAction = QtWidgets.QAction("&LEAVE", self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        # add the action to fileMenu
        fileMenu.addAction(extractAction)

        databaseMenu = mainMenu.addMenu('&Database')
        # create an action
        extractAction = QtWidgets.QAction("&Set Datbase", self)
        extractAction.setShortcut('Ctrl+O')
        extractAction.setStatusTip('Set database')
        extractAction.triggered.connect(self.open_database)
        # add the action to fileMenu
        databaseMenu.addAction(extractAction)

    def open_database(self):
        self.db = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a Database')
        self.label.setText('Selected Database: {}'.format(self.db))

    def close_application(self):
        print("bye")
        sys.exit()


# TEST CASE
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUi_MainWindow()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())

