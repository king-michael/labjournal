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

Infos:
 TabWidget:
    Actions:
        self.tabWidget.setCurrentWidget(tab)  # sets index of a current Tab
    Variables:
        self.tabWidget.indexOf(tab)  # index of a tab

Todo:
    - implement closeEvent(self, event):
        with write_settings()
        http://www.qtcentre.org/threads/20895-PyQt5-Want-to-connect-a-window-s-close-button
        https://doc.qt.io/archives/qt-4.8/qwidget.html#closeEvent
"""

__author__ = ["Michael King"]
__date__ = "29.09.2017"

import logging
import os
import sys

from PyQt5.QtCore import QSettings

from sqlalchemy.exc import OperationalError

from old_labjournal.gui.Ui_MainWindow import *
import old_labjournal.gui.tabs
import old_labjournal.gui.popups
import old_labjournal.core.databaseModel as databaseModel


logger = logging.getLogger('LabJournal')

APPLICATION_NAME = 'foo'
COMPANY_NAME = 'foo'
settings = QSettings(APPLICATION_NAME, COMPANY_NAME)

# =============================================================================#
# class GuiMainWindow
# =============================================================================#


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)  # where to display
        self._init_menubar()  # create the Menubar
        self.read_settings()  # Loads the settings

        # Tabwidget
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)  # make the first bar uncloseable
        self.tabWidget.tabCloseRequested.connect(self.tabWidget_TabCloseRequested)  # register close action
        self.tabWidget.currentChanged.connect(self.tabWidget_CurrentChanged)
        self.tabs = []  # set tab list to empty

        self.database_connect()  # Connect to a database, if there is one

    def _init_menubar(self):
        """Init function to create the Mainmenu"""
        # get the menuBar
        mainMenu = self.menuBar()

        # create a entry
        databaseMenu = mainMenu.addMenu('&File')
        # create an action (set Database)
        extractAction = QtWidgets.QAction("&Settings", self)  # Create a new Action
        extractAction.setStatusTip('Change Settings')  # set the StatusTip
        extractAction.triggered.connect(self.settings_open)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu

        # create a entry
        databaseMenu = mainMenu.addMenu('&Database')
        # create an action (set Database)
        extractAction = QtWidgets.QAction("&Set Database", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+O')  # set Shortcut
        extractAction.setStatusTip('Set database')  # set the StatusTip
        extractAction.triggered.connect(self.database_open)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu
        # create an action (create new Database)
        extractAction = QtWidgets.QAction("&Create New Datbase", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+Shift+N')  # set Shortcut
        extractAction.setStatusTip('Create a new database')  # set the StatusTip
        extractAction.triggered.connect(self.database_createNew)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu
        # create an action (disconnect from Database)
        extractAction = QtWidgets.QAction("&Disconnect from Datbase", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+Shift+D')  # set Shortcut
        extractAction.setStatusTip('Disconnect from current database')  # set the StatusTip
        extractAction.triggered.connect(self.database_disconnect)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu

    def _setup_LabJournalIndex_empty(self):
        """Creates the Empty LabJournalIndex"""
        if hasattr(self, 'MyWidget_LabJournalIndex'):  # if we are allready connected
            self.MyWidget_LabJournalIndex.deleteLater()  # send close command
        self.MyWidget_LabJournalIndex = QtWidgets.QPushButton('Select a Database')  # create a pushButton
        self.MyWidget_LabJournalIndex.clicked.connect(self.database_open)  # connect the pushButton to event
        self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)

    def settings_open(self):
        """
        Opens the Settings Dialog
        """
        dialog = old_labjournal.gui.popups.DialogSettings(self)
        dialog.show()

    def database_open(self):
        """
        Popup dialog to select a new Database
        """
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a Database')
        self.db = str(filename)  # fix because we get 'unicode' from PyQT5 and os.path cant handle it
        settings.setValue('Database/file', self.db)
        self.database_connect()

    def database_createNew(self):
        """
        Function to create an empty database
        """
        filename, _filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Select a Database')
        self.db = str(filename)  # fix because we get 'unicode' from PyQT5 and os.path cant handle it
        settings.setValue('Database/file', self.db)
        engine = databaseModel.create_engine('sqlite:///{}'.format(self.db))  # if we want spam
        databaseModel.Base.metadata.create_all(engine)
        self.database_connect()

    def database_connect(self):
        """
        Function to connect to the Database and create LabJournalIndex
        """
        # ToDo: Rewrite the try/except to check if the database is in the right format (atm we cant detect errors in LabJournalIndex)
        if os.path.exists(self.db):  # if the database exists
            try:
                if hasattr(self, 'MyWidget_LabJournalIndex'):  # if we are already connected
                    self.MyWidget_LabJournalIndex.deleteLater()  # send close command
                if hasattr(self, 'tabs'):                      # if we still have tabs open
                    self.tabWidget_closeAllTabs()              # close them
                self.MyWidget_LabJournalIndex = old_labjournal.gui.tabs.LabJournalTree(parent=self)
                self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)
                self.tabWidget_CurrentChanged(0)
                # Connect my Search
                self.MySearch_lineEdit.returnPressed.connect(self.search_resolve)
                self.MySearch_pushButton.clicked.connect(self.search_resolve)
                return
            except OperationalError as Err:
                settings.remove('Database/file')
                QtWidgets.QMessageBox.warning(self,
                                              'Warning',
                                              'Could not open:\n\n {}\n\nWrong database format.'.format(self.db))
                del self.db
                self._setup_LabJournalIndex_empty()  # in case we cant access a database create a start screen
                return

        self._setup_LabJournalIndex_empty()  # in case we cant access a database create a start screen

    def database_disconnect(self):
        """
        Function called when the database is closed
        """
        self.tabWidget_closeAllTabs()
        settings.remove('Database/file')
        self._setup_LabJournalIndex_empty()

    def database_createNewEntry(self):
        """
        Function called to create a new database entry
        """
        sim, result = old_labjournal.gui.popups.DialogNewEntry.getEntry()
        if result:
            session = databaseModel.establish_session('sqlite:///{}'.format(self.db))
            session.add(sim)
            session.commit()
            session.close()
            self.MyWidget_LabJournalIndex.build_tree()

    def read_settings(self):
        """
        Reads the Local Settings
        """
        self.db = str(settings.value('Database/file'))

    def write_settings(self):
        """Tobe Implemented"""
        pass

    def clear_layout(self, layout):
        """Deletes layouts to clean up"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def search_resolve(self):
        """Activate when Press enter in Search bar or hit button Search"""
        filtertext = self.MySearch_lineEdit.text()
        self.MyWidget_LabJournalIndex.lineEditFilter.setText(filtertext)

    def add_widget(self, widget, parent=None, uselayout=QtWidgets.QGridLayout):
        """
        Wrapper to add a widget
        Parameters
        ----------
        widget : QWidget
            widget i want to add
        parent : QWidget or QFrame or QMainWindow, None, optional
            in which parent i want to add it
        uselayout : QtWidget.QGridLayout, optional
            if the parent doesnt have a layout apply the following
        """

        if parent is None:             # if we don't get a parent use self
            parent = self
        layout = parent.layout()       # try to get the layout
        if layout is None:             # is we don't have a layout already use the defined one
            layout = uselayout(parent)
        layout.addWidget(widget)       # add the widget to the layout

    def labjournal_createTab(self, ID, entry_id=None, sim_type=None):
        """
        Open a new Tab for the LabJournal entry
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

    def tabWidget_createTab(self, name='newTab'):
        """
        Action to create a new Tab
        Notes
        -----
        stores the `tab` object and layout in self.tabs[`tab_ID`] = [`tab`, `layout`]
        with:
            tab : QtWidgets.QWidget()
                QtWidget, representing the `tab`
            layout : QGridLayout(tab)
                layout of the `tab`

        Parameters
        ----------
        name : str, optional
            name of the new `tab`. (Default is 'newTab')

        Returns
        -------
        tab_ID : int
            ID of the new created `tab`

        """


        """
        
        :param name: 
        :param tabWidget : name of the tabWiget Object [self.tabWidget]
        :return tabID
        """
        tab = QtWidgets.QWidget()  # create a new tab
        tab.setObjectName(name)  # set the displayed name
        layout = QtWidgets.QGridLayout(tab)  # set the layout

        self.tabWidget.addTab(tab, name)  # add tab to tabwidget
        self.tabs.append([tab, layout])  # store the tab and layout
        tab_ID = len(self.tabs) - 1  # tab id (-1 for Overview tab)

        return tab_ID

    def tabWidget_closeAllTabs(self):
        """
        Action to close all tabs
        """
        for (tab, layout) in self.tabs:  # iterate over all tabs
            tab.deleteLater()            # call destructor
        self.tabs = []                   # set tab list to empty

    def tabWidget_TabCloseRequested(self, currentIndex):
        """Action to close a tab"""

        currentQWidget = self.tabWidget.widget(currentIndex)  # get the current widget of the tab
        currentQWidget.deleteLater()  # register the widget for deletion
        self.tabs.pop(currentIndex - 1)  # remove the tab from the list
        self.tabWidget.removeTab(currentIndex)  # remove the tab

    def tabWidget_CurrentChanged(self, currentIndex):
        """Event when the Current Tab changes"""

        # Delete Old content
        for i in range(self.layout_sideMenu.count()):  # iterate over all childs in the layout_sideMenu
            child = self.layout_sideMenu.itemAt(i).widget()  # get the child
            child.deleteLater()  # register child for deletion

        # add new content
        currentQWidget = self.tabWidget.widget(currentIndex)  # get the current tab widget
        widget_in_tab = currentQWidget.layout().itemAt(0).widget()  # get the widget in the tab
        if hasattr(widget_in_tab, 'sideMenu_addContent'):  # check if it has the sideMenu_addContent method
            logger.debug("Create SideMenu: Entry")
            widget_in_tab.sideMenu_addContent(self)  # run the method


# =============================================================================#
# Tests
# =============================================================================#

if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)
    if not 'GUI' in locals():
        GUI = Main(False)  # fix to use in notebook
        app = GUI.start_app()
        window = GUI.start_window()
        GUI.show_gui()
    else:
        GUI.restart_gui()
    # FIXME: we need sys.exit(app.exec_()) or the plot from matplotlib will not be displayed
    sys.exit(app.exec_())
