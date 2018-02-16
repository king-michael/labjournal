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
import sys
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
        """TabWidget"""

        # make the first bar uncloseable
        self.tabWidget.tabBar().setTabButton(0, QtGui.QTabBar.RightSide, None)
        # register close action
        self.tabWidget.tabCloseRequested.connect(self.tabWidget_close_tab)


        self.connect_database()  # Connect to a database, if there is one



    def _init_menubar(self):
        """Init function to create the Mainmenu"""
        # get the menuBar
        mainMenu = self.menuBar()
        # create a entry
        databaseMenu = mainMenu.addMenu('&Database')
        # create an action
        extractAction = QtGui.QAction("&Set Datbase", self)
        extractAction.setShortcut('Ctrl+O')
        extractAction.setStatusTip('Set database')
        extractAction.triggered.connect(self.open_database)
        # add the action to fileMenu
        databaseMenu.addAction(extractAction)

    def open_database(self):
        """Dialog to select a database"""
        self.db = QtGui.QFileDialog.getOpenFileName(self, 'Select a Database')
        settings.setValue('Database/file', self.db)
        self.connect_database()

    def connect_database(self):
        """Function to connect to the Database and create LabJournalIndex"""
        if os.path.exists(self.db):  # if the database exists
            if hasattr(self,'MyWidget_LabJournalIndex'): # if we are allready connected
                self.MyWidget_LabJournalIndex.deleteLater()  # send close command
            self.MyWidget_LabJournalIndex = gui.tabs.LabJournalTree(parent=self)
            self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)
            # Connect my Search
            self.MySearch_lineEdit.returnPressed.connect(self.search_resolve)
            self.MySearch_pushButton.clicked.connect(self.search_resolve)
        elif not hasattr(self, 'MyWidget_LabJournalIndex'):  # if we are allready connected
            self.MyWidget_LabJournalIndex = QtGui.QPushButton('Select a Database')     # create a pushButton
            self.MyWidget_LabJournalIndex.clicked.connect(self.open_database)          # connect the pushButton to event                   # add
            self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)

    def readSettings(self):
        """Read the Settings"""
        self.db = settings.value('Database/file').toString()


    def writeSettings(self):
        """Tobe Implemented"""
        pass

    @QtCore.pyqtSlot()
    def on_btn_search_clicked(self):
        print(self.lineEditSide.text())

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
        if parent is None: parent = self
        layout = parent.layout()
        if layout is None:
            layout = uselayout(parent)
        layout.addWidget(widget)

    def create_tab_labjournal(self,ID,sim_id=None, sim_type=None):
        """Open a new Tab for the LabJournal entry"""

        name = sim_id if sim_id is not None else "New Tab"
        tabID = self.tabWidget_create_tab(name)
        if sim_type == 'LAMMPS':
            widget = gui.tabs.InfoEntry.LAMMPS(ID=ID,parent=self)
        else:
            widget = gui.tabs.InfoEntry.LAMMPS(ID=ID,parent=self)

        self.add_widget(widget, parent=self.tabs[tabID][0])
        self.tabWidget.setCurrentIndex(tabID+1) # +1 because 0 is maintab

    def tabWidget_create_tab(self,name='newTab'):
        """
        Action to create a new Tab
        stores the tab object and layout in
        self.tabs[tabID] = tab, layout
        :param name: name of the new tab [newTab]
        :param tabWidget : name of the tabWiget Object [self.tabWidget]
        :return tabID
        """
        if not hasattr(self,"tabs"):  # case we dont have a tabs dict
            self.tabs = {}
        if not hasattr(self,"tabs_lastID"):
            if len(self.tabs.keys()) == 0:  # case we dont have tabse
                self.tabs_lastID=-1
            else:  # case we have tabs stored, get the last ID
                self.tabs_lastID=sorted(self.tabs.keys())[-1]

        # Create Tab
        tab = QtGui.QWidget()  # create a new tab
        tab.setObjectName(QtCore.QString.fromUtf8(name))  # set the displayed name
        layout = QtGui.QGridLayout(tab)  # set the layout

        # add tab to tabwidget
        self.tabWidget.addTab(tab, QtCore.QString.fromUtf8(name))

        # Stores data
        tab_ID = self.tabs_lastID + 1  # increment tabs_lastID by one
        self.tabs[tab_ID] = tab, layout  # save tab,layout in dict
        self.tabs_lastID = tab_ID  # update tab id

        return tab_ID

    def tabWidget_close_tab(self, currentIndex):
        """Action to close a tab"""
        currentQWidget = self.tabWidget.widget(currentIndex)
        currentQWidget.deleteLater()
        self.tabWidget.removeTab(currentIndex)

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
