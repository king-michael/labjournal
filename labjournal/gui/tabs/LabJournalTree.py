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

import sys
from PyQt5 import QtCore, QtWidgets

from Ui_LabJournalTree import Ui_Form as Ui_TestWidget

sys.path.append("..")
from labjournal.core.databaseModel import *
from functools import partial
# BEGIN TESTS
import logging
logger = logging.getLogger('LabJournal')
logging.basicConfig(level=logging.DEBUG)

from PyQt5.QtCore import QSettings

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

class LabJournalTree(QtWidgets.QWidget, Ui_TestWidget):
    def __init__(self,parent=None):
        super(self.__class__,self).__init__(parent)
        self.parent = parent # get parent, allows communication about self.parent.ATTRIBUTES
        # Set up the user interface from Designer.

        self.setupUi(self)

        if parent is not None:
            self.db = self.parent.db
        else:
            self.db = settings.value('Database/file', '/home/micha/SIM-PhD-King/micha.db')

        # childmode: True if entries should have children, False if everything should be plain
        self.childmode=True

        # Build the tree
        self.build_tree()
        # create ContextMenu
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # set policity
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)  # connect the ContextMenuRequest

        # connect signal of lineEdit
        self.lineEditFilter.textChanged.connect(self.filter_tree)

    def add_item(self,child,sim):
        """
        :param child = QtWidgets.QTreeWidgetItem
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
        child = QtWidgets.QTreeWidgetItem(parent)
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

    def build_tree(self):
        """Function to create the tree"""
        # Create TableHeader
        columnheader = ['SimID', 'MediaWiki','description', 'tags', 'keywords', 'type']
        for i,header in enumerate(columnheader):
            self.treeWidget.headerItem().setText(i, header)
            self.treeWidget.clear()

        session = establish_session('sqlite:///{}'.format(self.db))
        logger.info("connect to database: {}".format(self.db))

        if self.childmode: # if my simulation can have childs
            parents  = session.query(Simulation).filter(not_(Simulation.parents.any())).all()
            #children = session.query(Simulation).filter(Simulation.parents.any()).all()
            # Fill the table #FIXME: do it with a database handler
            for row_number, sim in enumerate(parents):
                # Create an item and add it to the table
                parent = self.add_child2parent(sim,self.treeWidget)
                self.add_children2parent(sim,parent)
            self.treeWidget.expandAll() # expand by default

        else: # if everything should be plane
            rv = session.query(Simulation).all()
            # Fill the table #FIXME: do it with a database handler
            for row_number, sim in enumerate(rv):
                # Create an item and add it to the table
                QtWidgets.QTreeWidgetItem(self.treeWidget)
                child = self.treeWidget.topLevelItem(row_number)
                child = self.add_item(child,sim)

        # make the items clickable
        self.treeWidget.itemDoubleClicked.connect(self.event_itemDoubleClicked)
        # ToDo: add keyPressEvent
        # see add https://stackoverflow.com/questions/38507011/implementing-keypressevent-in-qwidget
        # adjust header size
        # Change size policty

        self.treeWidget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
        self.treeWidget.header().setSectionResizeMode(2, QtWidgets.QHeaderView.Interactive)
        self.treeWidget.header().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)
        self.treeWidget.header().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.treeWidget.header().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
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
        id = item.data(0,QtCore.Qt.UserRole) # returns tuple(int,bool) -> int = id
        if self.parent is not None:
            self.parent.labjournal_createTab(id,
                                             sim_id=item.text(0),
                                             sim_type=item.text(5))

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
            menu = QtWidgets.QMenu()
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
        # menu = QtWidgets.QMenu()
        # if level == 0:
        #     menu.addAction(self.tr("Edit person"))
        # elif level == 1:
        #     menu.addAction(self.tr("Edit object/container"))
        # elif level == 2:
        #     menu.addAction(self.tr("Edit object"))
        # menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

    def menu_change_type(self, item, column):
        """pop up menu to change the type"""
        text, ok = QtWidgets.QInputDialog.getText(self, 'set SIM type',
                                              'enter the sim type:',
                                              text=item.text(column))
        if ok:
            item.setText(column,text)

    def sideMenu_addContent(self,parent):
        """Creates Content in the sideMenu"""
        btn = QtWidgets.QPushButton("Create New Entry")  # create a pushButton for a new database Entry
        btn.clicked.connect(parent.database_createNewEntry)  # connect it to the event
        parent.layout_sideMenu.addWidget(btn)  # add the pushButton to the sideMenu

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LabJournalTree()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
