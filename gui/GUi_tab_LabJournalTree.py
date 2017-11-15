#!/usr/bin/env python
"""
# Details:
#   Wrapper around UiWidgetLabjournalTree.py
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

from __future__ import print_function
from PyQt4 import QtCore, QtGui
import sys

from UiWidgetLabjournalTree import Ui_Form as Ui_TestWidget

sys.path.append("..")
from core.Database import *
from core.logger import *
# BEGIN TESTS
log=Logger()

""" # IDEAS

# Make Items Changable
child->setFlags(child->flags() | Qt::ItemIsEnabled | Qt::ItemIsSelectable | Qt::ItemIsDragEnabled | Qt::ItemIsDropEnabled | Qt::ItemIsEditable);
child->setIcon(0,QIcon(":/Images/folder_pic.png"));


# Store Data in Item
QTreeWidgetItem* child = new QTreeWidgetItem();
child->setText(0, "New Folder");
[..]
int id = 1234;
double size = 12.34
child->setData(0, Qt::UserRole, id);
child->setData(0, Qt::UserRole + 1, size);
int id = child->data(0, Qt::UserRole).toInt();
double size = child->data(0, Qt::UserRole + 1).toDouble();
"""

class GUiWidgetLabjournalTree(QtGui.QWidget, Ui_TestWidget):
    def __init__(self,parent=None):
        super(self.__class__,self).__init__(parent)
        self.parent = parent # get parent, allows communication about self.parent.ATTRIBUTES
        # Set up the user interface from Designer.
        self.setupUi(self)

        try:
            self.DBAPI = self.parent.DBAPI
        except:
            log.info("Parents Don't have a database, use own")
            self.DBAPI = simpleAPI()
        self.tree_init()

        self.create_MyTable()
        self.lineEditFilter.textChanged.connect(self.filter_tree)

    def tree_init(self, parent=None):
        if parent is None: parent = self
        self.build_tree()
        # create ContextMenu
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # set policity
        self.treeWidget.customContextMenuRequested.connect(
            self.openMenu)  # connect the ContextMenuRequest

    def build_tree(self, table=None):  # << NEW
        """UpdateTree with file informations"""
        col = self.DBAPI.get_header_formated()
        if table is None: table = self.DBAPI.get_table_convert()
        for c in range(len(col)):
            self.treeWidget.headerItem().setText(c, col[c])
            self.treeWidget.clear()

        for item in range(len(table)):
            QtGui.QTreeWidgetItem(self.treeWidget)
            child = self.treeWidget.topLevelItem(item)
            for value in range(len(table[item])):
                # add displayed Value
                child.setText(value, str(table[item][value]))
                # add ToolTip
                child.setToolTip(value, str(table[item][value]))
            # set Data in the item (ID of the table)
            child.setData(0,QtCore.Qt.UserRole, item)

        # make the items clickable
        self.treeWidget.itemDoubleClicked.connect(self.event_itemDoubleClicked)
        # adjust header size

        self.treeWidget.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.treeWidget.header().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.treeWidget.header().setResizeMode(2, QtGui.QHeaderView.Stretch )
        self.treeWidget.header().setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        self.treeWidget.header().setStretchLastSection(True)




    def event_itemDoubleClicked(self,item, column_no):
        """Event when item is DoubleClicked"""
        # column_no = column_no  # Number of selected column
        # item.treeWidget().currentIndex().row()  # current index in table (changed by sorting)
        # item.treeWidget().currentIndex().column() # current column
        # item.data(0,QtCore.Qt.UserRole).toInt() # Data stored in item (ID for self.DBAPI.df)
        #       .toInt()  -> tuple(int,bool)
        #       .toDouble -> tuple(float,bool)
        #       .toString -> str(int)
        id = item.data(0,QtCore.Qt.UserRole).toInt()[0] # returns tuple(int,bool) -> int = id
        #print(item.)
        if self.parent is not None:
            self.parent.create_tab_labjournal(id)

    def hide_tree_items(self):
        """Hide all items in treeWidget"""
        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setHidden(True)

    def show_tree_items(self):
        """Show all items in treeWidget"""
        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setHidden(False)

    def filter_tree(self, filtertext=None):
        """Filter treeWidget"""
        if filtertext is None:
            filtertext = self.lineEditFilter.text()
        if len(filtertext) != 0:
            self.hide_tree_items()
            # ADDME: iterate over all columns add matches together, use them
            # list-of-QTreeWidgetItem QTreeWidget.findItems (self, QString, Qt.MatchFlags, int column = 0)
            # Returns a list of items that match the given text, using the given flags, in the given column.
            for item in self.treeWidget.findItems(filtertext,QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive):
                item.setHidden(False)
        else:
            self.show_tree_items()

    def create_MyTable(self, table=None):
        """Function to create the Table"""
        if not hasattr(self, 'MyTable_LabJournalIndex'):
            log('Initialize MyTable_LabJournalIndex')
            self.MyTable = QtGui.QTableWidget()
            # get columns
            col = self.DBAPI.get_header_formated()
            if table is None: table = self.DBAPI.get_table_convert()

            numcol = len(col)
            self.MyTable.setColumnCount(numcol)
            self.MyTable.setHorizontalHeaderLabels(col)  # set header
        else:
            numcol = self.MyTable.columnCount()

        numrow = len(table)
        self.MyTable.setRowCount(numrow)
        self.MyTable.clear()

        for r in range(numrow):
            for c in range(numcol):
                self.MyTable.setItem(r, c, QtGui.QTableWidgetItem(table[r][c]))

    def openMenu(self, position):
        """Function for rightclick on table entries"""
        indexes = self.treeWidget.selectedIndexes()
        level = -1
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GUiWidgetLabjournalTree()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
