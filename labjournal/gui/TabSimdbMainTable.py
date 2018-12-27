#!/usr/bin/env python
"""
TabSimdbMainTable
 - tab to display the Main table

SimdbTreeWidget
 - View how to display it
"""

from __future__ import print_function, absolute_import, generators


import logging

from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QSizePolicy,
                             QVBoxLayout,
                             QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt

from simdb.databaseModel import Main, create_engine, sessionmaker
from labjournal.gui.forms.Ui_LabJournalTree import Ui_Form


logger = logging.getLogger('LabJournal.TabSimdbMainTable')
"""Logger object `LabJournal.TabSimdbMainTable` for the tab."""

class SimdbTreeWidget(QWidget):
    def __init__(self, db=None, parent=None):
        super(SimdbTreeWidget, self).__init__(parent)
        self._header = ['entry_id', 'path', 'keywords', 'description', 'type']

        # define default parameters
        self.nested_mode = True  # Entries are nested.

        self.db = db
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        self.treeWidget = QTreeWidget()

        # set options
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setWordWrap(True)

        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)

        self.childItems = []

        logger.debug('created SimdbTreeWidget')
        self.header = self._header
        if db is not None:
            self.build_tree()


    @property
    def header(self):
        """
        Function get get the current header.

        Returns
        -------
        header : List[str]
            current header of the treeWidget
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        Function to set the current header of the treeWidget.

        Parameters
        ----------
        header : List[str]
            List of header items.

        Raises
        -------
        AssertionError
            If one of the items is not in the Maintable.
        """
        # sanity check
        assert all([h in Main.__dict__ for h in header]),  'invalid header\n:{}'.format(header)

        logger.debug('set header = {}'.format(header))
        self._header = header
        for i, header in enumerate(header):
            self.treeWidget.headerItem().setText(i, header)

    def map_tooltip(self, key, sim):
        """
        Mapping function to create the tooltip.
        Parameters
        ----------
        key : str
            keyword
        sim : Main
            Simulation object.

        Returns
        -------
        tooltip : str
            Tooltip for the keyword.
        """
        tooltip = ""
        if key in ['entry_id', 'path', 'description', 'type']:
            tooltip = "Url:\n {}\n".format(sim.url)+\
                      "Path:\n {}\n".format(sim.path)+\
                      "Details:\n {}".format(sim.description)
        elif key == 'keywords':
            tags = "\n ".join([key.name for key in sorted(sim.keywords, key=lambda x: x.name)
                              if key.value is None or key.value == 'None'])
            keywords = "\n ".join(["{} = {}".format(key.name, key.value)
                                    for key in sorted(sim.keywords, key=lambda x: x.name)
                                     if key.value is not None and key.value != 'None'])
            tooltip = "Tags:\n {}\nKeywords:\n {}".format(tags, keywords)
        return tooltip

    def fill_child(self, child, sim):
        """
        Function to fill the QTreeWidgetItem with informations.

        Parameters
        ----------
        child : QTreeWidgetItem
            child item ot fill with informations
        sim : Main
            Database Main object

        Returns
        -------
        child : QTreeWidgetItem
            return the child with new informations.
        """
        child.setData(0, Qt.UserRole, sim.id)  # set Data in the item (ID of the table)
        for i, key in enumerate(self.header):

            value = getattr(sim, key)

            if key == 'keywords':
                value = "; ".join(["{}={}".format(kw.name, kw.value)
                                   if kw.value is not None and kw.value != '' else kw.name
                                   for kw in sim.keywords])

            child.setText(i, value)
            child.setToolTip(i, self.map_tooltip(key, sim))

    def add_children2parent(self, sim, parent):
        """
        Function to add children to the parent.

        Parameters
        ----------
        sim : Main
            Simulation object
        parent : QTreeWidgetItem
            parent item
        """
        children = sim.children
        if len(children) == 0:
            return None
        for sim_child in children:
            child = QTreeWidgetItem(parent)
            self.fill_child(child=child, sim=sim_child.child)
            self.childItems.append(child)
            if len(sim_child.child.children) != 0:
                self.add_children2parent(sim=sim_child.child, parent=child)

    def build_tree(self):
        """
        Function to build the tree of the treewidget
        """
        logger.debug('build tree with nested_mode = {}'.format(self.nested_mode))

        sims = self.db.get_simulations(self.nested_mode)

        # Adding the child to the top level item
        for i, sim in enumerate(sims):
            child = QTreeWidgetItem(self.treeWidget)
            self.fill_child(child=child, sim=sim)
            self.childItems.append(child)
            if self.nested_mode and len(sim.children) != 0:
                self.add_children2parent(sim=sim, parent=child)

        # some general options
        self.treeWidget.sortByColumn(0, Qt.AscendingOrder)
        self.treeWidget.expandAll()

    def rebuild_tree(self):
        """
        Function to rebuild the treeWidget

        1. deletes all items
        2. set header
        3. build tree
        """
        self.clear_tree()
        self.header = self._header
        self.build_tree()

    def clear_tree(self):
        """
        Function to clear the tree.
        """
        root = self.treeWidget.invisibleRootItem()
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(0)
            (item.parent() or root).removeChild(item)
            del item

    def filter_tree(self, filtertext):
        """
        Function to filter the treeWidget.

        Parameters
        ----------
        filtertext : str
            Filter text
        """
        n_cols = len(self.header)
        if len(filtertext) != 0:
            logger.debug("filter for '{}'".format(filtertext))
            # hide all items
            for item in self.childItems:
                item.setHidden(True)

            for i in range(n_cols): # number of columns
                for item in self.treeWidget.findItems(filtertext,Qt.MatchContains | Qt.MatchRecursive, column=i):
                    item.setHidden(False) # turn items on again if they match
        else:
            # show items
            for item in self.childItems:
                item.setHidden(False)


class TabSimdbMainTable(QWidget, Ui_Form):
    def __init__(self, db=None, parent=None):
        super(TabSimdbMainTable, self).__init__(parent)

        self.setupUi(self)

        # setup options
        self.frameOptions.hide()
        self.optionShowOptions.toggled.connect(self.toggled_optionShowOptions)

        # treewidget
        self.treeWidget = SimdbTreeWidget(db=db, parent=self)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.optionParentView.setChecked(self.treeWidget.nested_mode)
        self.optionParentView.toggled.connect(self.toogle_optionParentView)
        self.layout().addWidget(self.treeWidget)

        self.searchLineEdit.textChanged.connect(self.treeWidget.filter_tree)
        self.searchLineEdit.returnPressed.connect(lambda : self.treeWidget.filter_tree(self.searchLineEdit.text()))

    def connect_database_SimdbTreeWdiget(self, db_thread):
        """
        Function to set the database to the treeWidget and rebuild the tree.

        Parameters
        ----------
        db_thread : Database
            QObject -> Database
        """
        self.treeWidget.db = db_thread.database
        self.treeWidget.rebuild_tree()

    def toggled_optionShowOptions(self, checked):
        """
        Function to show/hide the `frameOptions`.

        Parameters
        ----------
        checked : bool
            Show / hide `frameOptions`
        """
        if checked:
            self.frameOptions.show()
        else:
            self.frameOptions.hide()

    def toogle_optionParentView(self, checked):
        """
        Function to toggle the parent view.

        Parameters
        ----------
        checked : bool
            Toggle the parent view.
        """
        self.treeWidget.nested_mode = checked
        self.treeWidget.rebuild_tree()


if __name__ == '__main__':
    import sys

    # enable debuging
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    # try to apply coloring
    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        pass

    treeWidgetDialog = TabSimdbMainTable()
    treeWidgetDialog.show()
    #treeWidgetDialog.filter_tree("polymorphism")
    sys.exit(app.exec_())