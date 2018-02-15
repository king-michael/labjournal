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

from Ui_LabJournalTree import Ui_Form as Ui_TestWidget

sys.path.append("..")
from core.databaseModel import *
from functools import partial
# BEGIN TESTS
import logging
logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

from PyQt4.QtCore import QSettings

# ToDo: find a good organization / application name
# Todo: if added we can set the file path by ourself : https://stackoverflow.com/questions/4031838/qsettings-where-is-the-location-of-the-ini-file
settings = QSettings('foo', 'foo')

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

class LabJournalTree(QtGui.QWidget, Ui_TestWidget):
    def __init__(self,parent=None):
        super(self.__class__,self).__init__(parent)
        self.parent = parent # get parent, allows communication about self.parent.ATTRIBUTES
        # Set up the user interface from Designer.
        self.setupUi(self)

        # Build the tree
        self.build_tree()
        # create ContextMenu
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # set policity
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)  # connect the ContextMenuRequest

        # connect signal of lineEdit
        self.lineEditFilter.textChanged.connect(self.filter_tree)

    def add_item(self,child,sim):
        """
        :param child = QtGui.QTreeWidgetItem
        :param sim  = Simulation (object)
        :return: child
        """
        # create info entry
        info = "Mediawiki:\n {}\n\nPath:\n {}\n\nDetails:\n {}".format(sim.mediawiki,
                                                                       sim.path,
                                                                       sim.description)
        # SIM ID
        child.setText(0, str(sim.sim_id))
        child.setToolTip(0, str(info))
        # mediawiki
        child.setText(1, str(sim.mediawiki))
        child.setToolTip(1, str(info))
        # Details
        child.setText(2, str(sim.description))
        child.setToolTip(2, str(info))
        # tags
        tags = [key.name for key in sim.keywords.filter(Keywords.value.is_(None)).all()]
        child.setText(3, str("; ".join(tags)))
        child.setToolTip(3, str("\n".join(tags)))
        # keywords
        keywords = ["{}={}".format(key.name, key.value) for key in
                    sim.keywords.filter(not_(Keywords.value.is_(None))).all()]
        child.setText(4, str("; ".join(keywords)))
        child.setToolTip(4, str("\n".join(keywords)))
        # SIM TYPE
        child.setText(5, str(sim.sim_type))
        # store hidden data
        child.setData(0, QtCore.Qt.UserRole, sim.id)  # set Data in the item (ID of the table)
        return child

    def add_child2parent(self,sim,parent):
        child = QtGui.QTreeWidgetItem(parent)
        child = self.add_item(child, sim)
        return child

    def add_children2parent(self,sim,parent):
        children = sim.children.all()
        if len(children) == 0:
            return None
        for sim_child in children:
            child = self.add_child2parent(sim_child.child, parent)
            if len(sim_child.child.children.all()) !=0:
                self.add_children2parent(sim_child.child, child)
        return child

    def build_tree(self,childmode=True):
        """Function to create the tree"""
        # Create TableHeader
        columnheader = ['SimID', 'MediaWiki','description', 'tags', 'keywords', 'type']
        for i,header in enumerate(columnheader):
            self.treeWidget.headerItem().setText(i, header)
            self.treeWidget.clear()

        db = settings.value('Database/file', '/home/micha/SIM-PhD-King/micha.db').toString()
        logger.warn("WARNING: HARD CODED  default DATABASE in LabJournalTree.py")
        session = establish_session('sqlite:///{}'.format(db))
        logger.info("connect to database: {}".format(db))
        if childmode:
            parents  = session.query(Simulation).filter(not_(Simulation.parents.any())).all()
            #children = session.query(Simulation).filter(Simulation.parents.any()).all()
            # Fill the table #FIXME: do it with a database handler
            for row_number, sim in enumerate(parents):
                # Create an item and add it to the table
                parent = self.add_child2parent(sim,self.treeWidget)
                self.add_children2parent(sim,parent)
            self.treeWidget.expandAll() # expand by default

        else:
            rv = session.query(Simulation).all()
            # Fill the table #FIXME: do it with a database handler
            for row_number, sim in enumerate(rv):
                # Create an item and add it to the table
                QtGui.QTreeWidgetItem(self.treeWidget)
                child = self.treeWidget.topLevelItem(row_number)
                child = self.add_item(child,sim)

        # make the items clickable
        self.treeWidget.itemDoubleClicked.connect(self.event_itemDoubleClicked)
        # ToDo: add keyPressEvent
        # see add https://stackoverflow.com/questions/38507011/implementing-keypressevent-in-qwidget
        # adjust header size
        # Change size policty
        self.treeWidget.header().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.treeWidget.header().setResizeMode(1, QtGui.QHeaderView.Interactive)
        self.treeWidget.header().setResizeMode(2, QtGui.QHeaderView.Interactive)
        self.treeWidget.header().setResizeMode(3, QtGui.QHeaderView.Interactive)
        self.treeWidget.header().setResizeMode(4, QtGui.QHeaderView.Stretch)
        self.treeWidget.header().setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        self.treeWidget.header().setStretchLastSection(False)

        self.treeWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)

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

    def filter_tree(self, filtertext):
        """Filter treeWidget"""
        if len(filtertext) != 0:
            self.hide_tree_items() # hide all times
            for i in range(6): # number of columns
                for item in self.treeWidget.findItems(filtertext,QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, column=i):
                    item.setHidden(False) # turn items on again if they match
        else:
            self.show_tree_items()

    def openMenu(self, position):
        """Function for rightclick on table entries"""

        item = self.treeWidget.currentItem()
        column = self.treeWidget.currentColumn()
        if column in [2, 3, 4]:
            menu = QtGui.QMenu()
            # column dependent action
            if column == 2:
                action = menu.addAction(self.tr("edit tags"))

            elif column == 3:
                action = menu.addAction(self.tr("edit keywords"))
            elif column == 4:
                action = menu.addAction(self.tr("edit type"))
                action.triggered.connect(partial(self.menu_change_type,
                                                 item=item,
                                                 column=column))

            menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        # HANDLE PARENTS AND CHILDS
        # indexes = self.treeWidget.selectedIndexes()
        # level = -1
        # if len(indexes) > 0:
        #
        #     level = 0
        #     index = indexes[0]
        #     while index.parent().isValid():
        #         index = index.parent()
        #         level += 1
        #
        # menu = QtGui.QMenu()
        # if level == 0:
        #     menu.addAction(self.tr("Edit person"))
        # elif level == 1:
        #     menu.addAction(self.tr("Edit object/container"))
        # elif level == 2:
        #     menu.addAction(self.tr("Edit object"))
        # menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

    def menu_change_type(self, item, column):
        """pop up menu to change the type"""
        text, ok = QtGui.QInputDialog.getText(self, 'set SIM type',
                                              'enter the sim type:',
                                              text=item.text(column))
        if ok:
            item.setText(column,text)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = LabJournalTree()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
