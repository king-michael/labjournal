from __future__ import print_function, division, generators, nested_scopes
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QFrame,
                             QVBoxLayout, QHBoxLayout,
                             QLabel, QToolButton,
                             QTreeView,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, QModelIndex
from labjournal.gui.QtExtensions import FlowLayout

from simdb.databaseModel import Keywords, Main, create_engine, sessionmaker
import sys

class DatabaseTreeView(QWidget):
    """
    ToDo
    ----
    setSelectionBehavior
        # Maybe change this to select items for further utilities
        QAbstractItemView.SelectRows vs QAbstractItemView.SelectItems
    """
    def __init__(self):
        """

        Parameters
        ----------
        header : List[str]
            List of header entries.

        Arguments
        ---------
        nested_mode : bool
            If the view is nested or flatten. (Default is False)
        """
        super(QWidget, self).__init__()

        self.header = ['entry_id', 'path', 'keywords', 'description', 'type']
        self.id_keywords = self.header.index('keywords') if 'keywords' in self.header else None
        # define default parameters
        self.nested_mode = True   # Entries are nested.

        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        # create tree
        self.tree = QTreeView()
        self.vboxLayout.addWidget(self.tree)

        # set parameters
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(True)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.set_header(self.header)
        self.build_tree()

    def set_header(self, header):
        """
        Wrapper to set the header of the TreeView
        Parameters
        ----------
        header : List["str"]
            List of header entries.
        """
        self.header = header
        self.id_keywords = self.header.index('keywords') if 'keywords' in self.header else None
        self.model.setHorizontalHeaderLabels(header)

    def _create_row(self, i, sim, old_list=()):

        my_list = list(old_list)
        my_list.append(i)
        list_keywords = []

        # build row
        list_row = [QStandardItem(
            str(getattr(sim, attr) if attr != 'keywords' else ', '.join(
                ["{}={}".format(k.name, k.value) if k.value != 'None' else k.name for k in sim.keywords]))
            ) for attr in self.header]

        # set parent attributes
        for parent in list_row:
            parent.setFlags(Qt.NoItemFlags)

        # add children
        if self.nested_mode and len(sim.children) > 0:
            for j, child in enumerate(sorted(sim.children, key=lambda x: x.child.entry_id)):
                child_row = self._create_row(j, child.child, old_list=my_list)
                list_row[0].appendRow(child_row)

        return list_row

    def build_tree(self):
        """
        Function to build the treeview.
        """

        # EXPERIMENTAL
        db_path = 'micha_raw.db'

        engine = create_engine('sqlite:///{}'.format(db_path))
        Session = sessionmaker(bind=engine)
        session = Session()

        if self.nested_mode:
            sims = session.query(Main).join().filter(~Main.parents.any()).order_by(Main.entry_id).all()
        else:
            sims = session.query(Main).order_by(Main.entry_id).all()

        for i, sim in enumerate(sims):
            list_row = self._create_row(i, sim)
            self.model.appendRow(list_row)

        self.tree.expandAll()


class SimpleTreeView(QWidget):
    def __init__(self):
        super(SimpleTreeView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        # Tree view
        self.tree_widget = DatabaseTreeView()
        self.vboxLayout.addWidget(self.tree_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeView()
    treeWidgetDialog.show()
    sys.exit(app.exec_())