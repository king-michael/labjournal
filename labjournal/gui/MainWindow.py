#!/usr/bin/env python
"""
# Details:
#   GuiMainWindow
# Authors:
#   Michael King <michael.king@uni-konstanz.de>
# History:
#   -
# Last modified: 29.09.2017
# ToDo:
#   -
# Bugs:
#   -
"""

from __future__ import absolute_import, print_function, division, nested_scopes, generators

__author__ = ["Michael King"]
__date__ = "22.11.2018"

import logging
import os
import sys

<<<<<<< Updated upstream
from functools import partial

from PyQt5.QtWidgets import (QMainWindow,
                             QTabBar,
                             QAction,
                             QFileDialog,
                             QMessageBox)
=======
from PyQt5.QtWidgets import (QMainWindow, QTabBar,
                             QWidget,
                             QGridLayout)
from PyQt5.QtCore import Qt
from labjournal.gui.forms.Ui_MainWindow import Ui_MainWindow
from labjournal.gui.TabSimdbMainTable import TabSimdbMainTable
>>>>>>> Stashed changes

from labjournal.gui.forms.Ui_MainWindow import Ui_MainWindow
from labjournal.gui.TabSimdbMainTable import TabSimdbMainTable
from labjournal.gui.DatabaseAPI import DatabaseThread
logger = logging.getLogger('LabJournal')

# =============================================================================#
# class MainWindow
# =============================================================================#


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
<<<<<<< Updated upstream

        self.db_path = 'micha_raw.db'
=======
>>>>>>> Stashed changes

        # load display
        self.setupUi(self)


        # Tabwidget
        self.tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)  # make the first bar uncloseable
        #self.tabWidget.tabCloseRequested.connect(self.tabWidget_TabCloseRequested)  # register close action
        #self.tabWidget.currentChanged.connect(self.tabWidget_CurrentChanged)
        self._tabs = []  # set tab list to empty
        self._entry_index2tab = {}

        self._setup_mainMenu()

        self.setup_tabMainTable()
        self.connect_databaseThread(self.db_path)

    def connect_databaseThread(self, db_path, new_database=False):
        """
        Function to connect to the databaseThread.

        sets ``self.self.databaseThread``.

        Parameters
        ----------
        db_path : str
            Path of the database.
        new_database : bool
            Switch if this is a new database.
        """
        self.db_path = db_path
        self.databaseThread = DatabaseThread(db_path=self.db_path, new_database=new_database)
        self.databaseThread.start()
        self.databaseThread.connected.connect(partial(self.tabSimdbMainTable.connect_database_SimdbTreeWdiget,
                                                      db_thread=self.databaseThread))

    def disconnect_databaseThread(self):
        """
        Function to disconnect from the databaseThread.
        """
        self.databaseThread.running = False
        self.databaseThread.wait()
        del self.databaseThread

    def setup_tabMainTable(self):
        """
        Function to fill the tab `MainTable`
        """
<<<<<<< Updated upstream

        self.tabSimdbMainTable = TabSimdbMainTable(db=None,
                                                   parent=self)

        layout = self.tab_MainTable.layout()
        layout.addWidget(self.tabSimdbMainTable)

    def _setup_mainMenu(self):
        """
        Function to create the MainMenu
        """

        mainMenu = self.menuBar()

        # create a entry
        databaseMenu = mainMenu.addMenu('&Database')
        # create an action (set Database)
        extractAction = QAction("&Open Database", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+O')  # set Shortcut
        extractAction.setStatusTip('Open database')  # set the StatusTip
        extractAction.triggered.connect(self.action_open_database)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu

        # create an action (create new Database)
        extractAction = QAction("&Create New Database", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+Shift+N')  # set Shortcut
        extractAction.setStatusTip('Create a new database')  # set the StatusTip
        extractAction.triggered.connect(self.action_create_new_database)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu

        # create an action (disconnect from Database)
        extractAction = QAction("&Disconnect from Database", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+Shift+D')  # set Shortcut
        extractAction.setStatusTip('Disconnect from current database')  # set the StatusTip
        extractAction.triggered.connect(self.action_disconnect_database)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu

    def action_open_database(self):
        """
        Popup dialog to select a new Database
        """
        filename, _filter = QFileDialog.getOpenFileName(self,
                                                        'Select a Database')
        db_path = str(filename)  # fix because we get 'unicode' from PyQT5 and os.path cant handle it

        if not os.path.exists(db_path):  # if the database exists
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("File {} not found.".format(db_path))
            msg.setWindowTitle('Error')
            return
        if hasattr(self, 'databaseThread'):
            self.disconnect_databaseThread()

        self.connect_databaseThread(db_path, new_database=False)

    def action_create_new_database(self):
        filename, _filter = QFileDialog.getSaveFileName(self, 'Select a Database')
        db_path = str(filename)  # fix because we get 'unicode' from PyQT5 and os.path cant handle it

        if hasattr(self, 'databaseThread'):
            self.disconnect_databaseThread()

        self.connect_databaseThread(db_path, new_database=True)

    def action_disconnect_database(self):
        """
        Function called when the database is closed
        """
        self.tabWidget_close_all_tabs()
        if hasattr(self, 'databaseThread'):
            self.disconnect_databaseThread()
        self.tabSimdbMainTable.treeWidget.clear_tree()

    def tabWidget_close_all_tabs(self):
        """
        Action to close all tabs
        """
        for (tab, layout) in self.tabs:  # iterate over all tabs
            tab.deleteLater()            # call destructor
        self.tabs = []                   # set tab list to empty
=======
        self.tabSimdbMainTable = TabSimdbMainTable(self)
        self.tabSimdbMainTable.treeWidget.treeWidget.itemDoubleClicked.connect(self.treeWidget_itemDoubleClicked)
        layout = self.tab_MainTable.layout()
        layout.addWidget(self.tabSimdbMainTable)

    def treeWidget_itemDoubleClicked(self,item, column_no):
        """Event when item is DoubleClicked"""
        # column_no = column_no  # Number of selected column
        # item.treeWidget().currentIndex().row()  # current index in table (changed by sorting)
        # item.treeWidget().currentIndex().column() # current column
        # item.data(0,QtCore.Qt.UserRole).toInt() # Data stored in item (ID for self.DBAPI.df)
        #       .toInt()  -> tuple(int,bool)
        #       .toDouble -> tuple(float,bool)
        #       .toString -> str(int)


        id = item.data(0,Qt.UserRole) # returns tuple(int,bool) -> int = id
        entry_id = item.text(0)
        entry_type = item.text(4) # THIS MAY BREAK THE CODE IN THE FUTURE if the header is changed
        logger.debug('treeWidget_itemDoubleClicked : {}'.format(id))
        print(id, entry_id, entry_type)

    def create_new_tab_entry(self, index, entry_id=None, sim_type=None):
        """
        Function to create a new tab for a entry.
        Parameters
        ----------
        id : int
            Id of the Main table.

        Returns
        -------

        """

        name = entry_id if entry_id is not None else "New Tab"
        tabID = self.tabWidget_createTab(name)
        if sim_type == 'LAMMPS':
            widget = old_labjournal.gui.tabs.InfoEntry.LAMMPS(ID=ID, parent=self)
        elif sim_type == 'GROMACS':
            widget = old_labjournal.gui.tabs.InfoEntry.GROMACS(ID=ID, parent=self)
        else:
            widget = old_labjournal.gui.tabs.InfoEntry.InfoEntry(ID=ID, parent=self)

        self.add_widget(widget, parent=self.tabs[tabID][0])
        self.tabWidget.setCurrentIndex(tabID + 1)  # +1 because 0 is maintab

    def create_new_tab(self, name='newTab'):
        """
        Function to create a new Tab.

        Notes
        -----
        stores the `tab` object and layout in self.tabs[`tab_ID`] = [`tab`, `layout`]


        Parameters
        ----------
        name : str, optional
            name of the new `tab`. (Default is 'newTab')

        Returns
        -------
        tab_ID : int
            ID of the new created `tab`

        """

        tab = QWidget()  # create a new tab
        tab.setObjectName(name)  # set the displayed name
        layout = QGridLayout(tab)  # set the layout

        self.tabWidget.addTab(tab, name)  # add tab to tabwidget
        self.tabs.append([tab, layout])  # store the tab and layout
        tab_ID = len(self.tabs) - 1  # tab id (-1 for Overview tab)

        return tab_ID

>>>>>>> Stashed changes


# =============================================================================#
# Tests
# =============================================================================#

if __name__ == '__main__':
    # enable debuging
    logging.basicConfig(level=logging.DEBUG)

    # add module to path
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))
    from PyQt5.QtWidgets import QApplication

    # create the window and start it
    app = QApplication(sys.argv)

    # try to apply coloring
    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        pass

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
