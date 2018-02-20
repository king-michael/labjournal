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
        with writeSettings()
        http://www.qtcentre.org/threads/20895-PyQt4-Want-to-connect-a-window-s-close-button
        https://doc.qt.io/archives/qt-4.8/qwidget.html#closeEvent
"""

__author__ = ["Michael King"]
__date__ = "29.09.2017"

# BEGIN Import System Packages
import sys, os
import logging
from PyQt4 import QtGui
from PyQt4.QtCore import QSettings

logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

settings = QSettings('foo', 'foo')

# END Import System Packages


# BEGIN Import GuiApplications
from Ui_MainWindow import *
import gui.tabs
import popups
# END Import GuiApplications
# my modules
sys.path.append('..')
from core import *
settings = QSettings('foo', 'foo')

class Main:
    def __init__(self, state=True):
        """MainClass"""
        if state:
            self.start_app()
            self.start_window()
            self.show_gui()

    def start_app(self):
        self.app = QtGui.QApplication(sys.argv)
        return self.app

    def start_window(self):
        self.window = MainWindow()
        # setup stylesheet
        try:
            import qdarkstyle  # style
            self.app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
        except:
            pass
        return self.window

    def show_gui(self):
        self.window.show()

    def restart_gui(self):
        self.start_window()
        self.show_gui()

    def __del__(self):
        '''Destruction of class'''
        sys.exit(app.exec_())
# END TESTS

#=============================================================================#
# class GuiMainWindow
#=============================================================================#


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)    # where to display
        self._init_menubar()  # create the Menubar
        self.readSettings()   # Loads the settings

        # Tabwidget
        self.tabWidget.tabBar().setTabButton(0, QtGui.QTabBar.RightSide, None)  # make the first bar uncloseable
        self.tabWidget.tabCloseRequested.connect(self.tabWidget_TabCloseRequested)      # register close action
        self.tabWidget.currentChanged.connect(self.tabWidget_CurrentChanged)

        self.database_connect()  # Connect to a database, if there is one

    def _init_menubar(self):
        """Init function to create the Mainmenu"""
        # get the menuBar
        mainMenu = self.menuBar()
        # create a entry
        databaseMenu = mainMenu.addMenu('&Database')
        # create an action (set Database)
        extractAction = QtGui.QAction("&Set Database", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+O')                  # set Shortcut
        extractAction.setStatusTip('Set database')           # set the StatusTip
        extractAction.triggered.connect(self.database_open)  # connect it to an function
        databaseMenu.addAction(extractAction)                # add the action to fileMenu
        # create an action (create new Database)
        extractAction = QtGui.QAction("&Create New Datbase", self)  # Create a new Action
        extractAction.setShortcut('Ctrl+Shift+N')  # set Shortcut
        extractAction.setStatusTip('Create a new database')  # set the StatusTip
        extractAction.triggered.connect(self.database_createNew)  # connect it to an function
        databaseMenu.addAction(extractAction)  # add the action to fileMenu


    def database_open(self):
        """Dialog to select a database"""
        self.db = QtGui.QFileDialog.getOpenFileName(self, 'Select a Database')
        settings.setValue('Database/file', self.db)
        self.database_connect()

    def database_createNew(self):
        """Create an empty database"""
        self.db = QtGui.QFileDialog.getSaveFileName(self, 'Select a Database')
        settings.setValue('Database/file', self.db)
        engine = databaseModel.create_engine('sqlite:///{}'.format(self.db))  # if we want spam
        databaseModel.Base.metadata.create_all(engine)
        self.database_connect()

    def database_connect(self):
        """Function to connect to the Database and create LabJournalIndex"""
        if os.path.exists(self.db):  # if the database exists
            if hasattr(self,'MyWidget_LabJournalIndex'): # if we are allready connected
                self.MyWidget_LabJournalIndex.deleteLater()  # send close command
            self.MyWidget_LabJournalIndex = gui.tabs.LabJournalTree(parent=self)
            self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)
            # Connect my Search
            self.MySearch_lineEdit.returnPressed.connect(self.search_resolve)
            self.MySearch_pushButton.clicked.connect(self.search_resolve)
            self.MyWidget_LabJournalIndex.sideMenu_addContent(self)
        elif not hasattr(self, 'MyWidget_LabJournalIndex'):  # if we are allready connected
            self.MyWidget_LabJournalIndex = QtGui.QPushButton('Select a Database')     # create a pushButton
            self.MyWidget_LabJournalIndex.clicked.connect(self.database_open)          # connect the pushButton to event                   # add
            self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)

    def database_createNewEntry(self):
        """Create a new Database entry"""
        sim, result = popups.DialogNewEntry.getEntry()
        if result:
            session = databaseModel.establish_session('sqlite:///{}'.format(self.db))
            session.add(sim)
            session.commit()
            session.close()
            self.MyWidget_LabJournalIndex.build_tree()

    def readSettings(self):
        """Read the Settings"""
        self.db = settings.value('Database/file').toString()



    def writeSettings(self):
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

    def add_widget(self, widget, parent=None, uselayout=QtGui.QGridLayout):
        """Wrapper to add a widget
        add_widget(widget,parent=None,uselayout=QtGui.QGridLayout)
        widget : widget i want to add
        parent : in which parent i want to add it
        uselayout : if the parent doesnt have a layout apply the following
        """
        if parent is None:
            parent = self
        layout = parent.layout()
        if layout is None:
            layout = uselayout(parent)
        layout.addWidget(widget)

    def labjournal_createTab(self, ID, sim_id=None, sim_type=None):
        """Open a new Tab for the LabJournal entry"""

        name = sim_id if sim_id is not None else "New Tab"
        tabID = self.tabWidget_createTab(name)
        if sim_type == 'LAMMPS':
            widget = gui.tabs.InfoEntry.LAMMPS(ID=ID,parent=self)
        else:
            widget = gui.tabs.InfoEntry.InfoEntry(ID=ID,parent=self)

        self.add_widget(widget, parent=self.tabs[tabID][0])
        self.tabWidget.setCurrentIndex(tabID+1) # +1 because 0 is maintab

    def tabWidget_createTab(self,name='newTab'):
        """
        Action to create a new Tab
        stores the tab object and layout in
        self.tabs[tabID] = tab, layout
        :param name: name of the new tab [newTab]
        :param tabWidget : name of the tabWiget Object [self.tabWidget]
        :return tabID
        """
        if not hasattr(self, "tabs"):  # init self.tabs if not there
            self.tabs = []

        tab = QtGui.QWidget()  # create a new tab
        tab.setObjectName(QtCore.QString.fromUtf8(name))  # set the displayed name
        layout = QtGui.QGridLayout(tab)  # set the layout

        self.tabWidget.addTab(tab, QtCore.QString.fromUtf8(name))  # add tab to tabwidget
        self.tabs.append([tab, layout])  # store the tab and layout
        tab_ID = len(self.tabs) - 1  # tab id (-1 for Overview tab)

        return tab_ID

    def tabWidget_TabCloseRequested(self, currentIndex):
        """Action to close a tab"""

        currentQWidget = self.tabWidget.widget(currentIndex)  # get the current widget of the tab
        currentQWidget.deleteLater()   # register the widget for deletion
        self.tabs.pop(currentIndex-1)  # remove the tab from the list
        self.tabWidget.removeTab(currentIndex)  # remove the tab

    def tabWidget_CurrentChanged(self,currentIndex):
        """Event when the Current Tab changes"""

        # Delete Old content
        for i in range(self.layout_sideMenu.count()):  # iterate over all childs in the layout_sideMenu
            child = self.layout_sideMenu.itemAt(i).widget()  # get the child
            child.deleteLater()  # register child for deletion

        # add new content
        currentQWidget = self.tabWidget.widget(currentIndex)  # get the current tab widget
        widget_in_tab=currentQWidget.layout().itemAt(0).widget()  # get the widget in the tab
        if hasattr(widget_in_tab, 'sideMenu_addContent'):  # check if it has the sideMenu_addContent method
            logger.debug("Create SideMenu: Entry")
            widget_in_tab.sideMenu_addContent(self)  # run the method

#=============================================================================#
# Tests
#=============================================================================#

if __name__ == '__main__':
    if not 'GUI' in locals():
        GUI = Main(False)  # fix to use in notebook
        app = GUI.start_app()
        window = GUI.start_window()
        GUI.show_gui()
    else:
        GUI.restart_gui()
    # FIXME: we need sys.exit(app.exec_()) or the plot from matplotlib will not be displayed
    sys.exit(app.exec_())
