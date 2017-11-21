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
"""

from __future__ import print_function
import sys
from PyQt4 import QtCore

# END Import System Packages

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# BEGIN Import GuiApplications
from Ui_MainWindow import *
import gui.tabs
# END Import GuiApplications
# my modules
sys.path.append('..')
from core import *
from core.logger import Logger

__author__              = ["Michael King"]
__date__                = "29.09.2017"



# Text Handling
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# BEGIN TESTS
log = Logger()



class main():
    def __init__(self, state=True):
        '''MainClass'''
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
        self.setupUi(self)  # where to display

        self.DBAPI = simpleAPI()

        """TabWidget"""
        # make the first bar uncloseable
        self.tabWidget.tabBar().setTabButton(0, QtGui.QTabBar.RightSide, None)
        # register close action
        self.tabWidget.tabCloseRequested.connect(self.tabWidget_close_tab)

        """Register the GUiWidgetLabjournalTree in MyTabLabJournalIndex"""
        self.MyWidget_LabJournalIndex = gui.tabs.LabJournalTree(parent=self)
        self.add_widget(self.MyWidget_LabJournalIndex, parent=self.MyTabLabJournalIndex)

        """register_actions"""
        # Buttons
        #self.btn_cal.clicked.connect(self.create_editor)
        #self.btn_clear.clicked.connect(self.clear_frameTEST)
        #self.btn_mine.clicked.connect(self.on_btn_search_clicked)

        # MySearch
        self.MySearch_lineEdit.returnPressed.connect(self.search_resolve)
        self.MySearch_pushButton.clicked.connect(self.search_resolve)

        self.pushButton_3.setText("Save db -> SQL (tmp.db)")
        self.pushButton_3.clicked.connect(self.DBAPI.save_sql)


    @QtCore.pyqtSlot()
    def on_btn_search_clicked(self):
        print(self.lineEditSide.text())

    def clear_layout(self, layout):
        '''Deletes layouts to clean up'''
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def search_resolve(self):
        '''Activate when Press enter in Search bar or hit button Search'''
        filtertext = self.MySearch_lineEdit.text()
        self.MyWidget_LabJournalIndex.filter_tree(filtertext)

    def add_widget(self, widget, parent=None, uselayout=QtGui.QGridLayout):
        '''Wrapper to add a widget
        add_widget(widget,parent=None,uselayout=QtGui.QGridLayout)
        widget : widget i want to add
        parent : in which parent i want to add it
        uselayout : if the parent doesnt have a layout apply the following
        '''
        if parent is None: parent = self
        layout = parent.layout()
        if layout is None:
            layout = uselayout(parent)
        layout.addWidget(widget)

    def create_tab_labjournal(self,ID):
        """Open a new Tab for the LabJournal entry"""

        name = self.DBAPI.df.loc[ID,'simid']
        tabID = self.tabWidget_create_tab(name)
        widget = gui.tabs.InfoEntry(ID=ID, parent=self)

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
        GUI = main(False)  # fix to use in notebook
        app = GUI.start_app()
        window = GUI.start_window()
        GUI.show_gui()
    else:
        GUI.restart_gui()

