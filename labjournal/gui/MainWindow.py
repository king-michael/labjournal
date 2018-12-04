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

from labjournal.gui.Ui_MainWindow import *
from labjournal.gui.TabSimdbMainTable import TabSimdbMainTable

logger = logging.getLogger('LabJournal')

# =============================================================================#
# class MainWindow
# =============================================================================#


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # load display
        self.setupUi(self)

        mainMenu = self.menuBar()

        # Tabwidget
        self.tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, None)  # make the first bar uncloseable
        #self.tabWidget.tabCloseRequested.connect(self.tabWidget_TabCloseRequested)  # register close action
        #self.tabWidget.currentChanged.connect(self.tabWidget_CurrentChanged)
        self.tabs = []  # set tab list to empty

        self.setup_tabMainTable()

    def setup_tabMainTable(self):
        """
        Function to fill the tab `MainTable`
        """
        self.tabSimdbMainTable = TabSimdbMainTable(self)
        layout = self.tab_MainTable.layout()
        layout.addWidget(self.tabSimdbMainTable)



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
