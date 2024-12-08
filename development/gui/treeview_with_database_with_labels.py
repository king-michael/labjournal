from __future__ import print_function, division, generators, nested_scopes
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QFrame,
                             QVBoxLayout, QHBoxLayout, QLayout,
                             QLabel, QToolButton,
                             QTreeView,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, QModelIndex
from labjournal.gui.QtExtensions import FlowLayout

from simdb.databaseModel import Keywords, Main, create_engine, sessionmaker
import sys


# TODO: fix FlowLayout -> resize coulumn height

class KeywordLabel(QLabel):
    def __init__(self,keyword='', value=None, parent=None):
        super(QLabel, self).__init__(parent)

        stylesheet = " ".join([
            'font-size:8pt;',
            'border-radius: 10px;',
            'background-color: #00a9e0;',
            'padding: 0px 10px 0px;'
            'color: white;',
        ])
        self.setStyleSheet(stylesheet)

        #self.setMinimumSize(QSize(40, 40))
        self.setAlignment(Qt.AlignCenter)
        self.setTextFormat(Qt.RichText)
        # set text
        if value is None or value == 'None':
            text = "<b>{}</b>".format( keyword)
        else:
            text = "{}<br><b>{}</b>".format(keyword, value)
        self.setText(text)

class TagSymbol(QToolButton):
    def __init__(self, keyword='', value=None, parent=None):
        """
        Plus Button for adding tags or keywords

        Parameters
        ----------
        text : str
            Text to be displayed
        parent : QtWidget(InfoEntry)
            parent of the tag (connect method to it)
        """

        super(QToolButton, self).__init__()

        self.parent = parent  # save parent

        font_size_big = 10
        font_size_small = 6
        stylesheet = " ".join([
            'border-radius: 10px;',
            'background-color: #00a9e0;',
            'color: white;'
            'margin-left: 10px;',
            'margin-right: 10px;'
        ])

        # set text
        if value is None or value == 'None':
            text = "<span style='font-size:{}pt; font-weight:600;'>{}</span>".format(font_size_big, keyword)
        else:
            text = "<span style='font-size:{}pt; font-weight:600;'>\n{}</span><br>".format(font_size_small, keyword)
            text += "<span style='font-size:{}pt; font-weight:600;'>{}</span>".format(font_size_big, value)

        # setup the tag symbol
        self.setText(text)
        # font = self.font()
        # font.setBold(True)
        # self.setFont(font)

        self.setStyleSheet(stylesheet)

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

    def _create_keywords_labels(self, keywords):
        """
        Function to create the labels for keywords
        Parameters
        ----------
        keywords : List[Keywords]
            List of keywords

        Returns
        -------
        frame : QFrame
            Frame with all the labels in it.
        """

        frame = QFrame()
        layout = FlowLayout()
        # layout.setAlignment(Qt.AlignVCenter)
        # layout.setSizeConstraint(QLayout.SetMinimumSize)
        frame.setLayout(layout)
        for i, keyword in enumerate(keywords):
            label = KeywordLabel(keyword=keyword.name, value=keyword.value)
            frame.layout().addWidget(label)
        return frame

    def _create_row(self, i, sim, old_list=()):

        my_list = list(old_list)
        my_list.append(i)
        list_keywords = []

        # build row
        list_row = [QStandardItem(str(getattr(sim, attr) if attr != 'keywords' else ''))
                    for attr in self.header]

        # set parent attributes
        for parent in list_row:
            parent.setFlags(Qt.NoItemFlags)

        # add keywords
        if self.id_keywords is not None and len(sim.keywords) != 0:
            list_keywords.append([tuple(my_list), sim.keywords])

        # add children
        if self.nested_mode and len(sim.children) > 0:
            for j, child in enumerate(sorted(sim.children, key=lambda x: x.child.entry_id)):
                child_row, child_keywords = self._create_row(j, child.child, old_list=my_list)
                list_keywords.extend(child_keywords)
                list_row[0].appendRow(child_row)

        return list_row, list_keywords

    def build_tree(self):
        """
        Function to build the treeview.
        """

        # EXPERIMENTAL
        db_path = 'micha_raw.db'

        engine = create_engine('sqlite:///{}'.format(db_path))
        Session = sessionmaker(bind=engine)
        session = Session()

        list_keywords = []

        if self.nested_mode:
            sims = session.query(Main).join().filter(~Main.parents.any()).order_by(Main.entry_id).all()
        else:
            sims = session.query(Main).order_by(Main.entry_id).all()

        for i, sim in enumerate(sims):
            list_row, sublist_keywords = self._create_row(i, sim)
            list_keywords.extend(sublist_keywords)
            self.model.appendRow(list_row)

        for index_tuple, keywords in list_keywords:
            frame = self._create_keywords_labels(keywords=keywords)
            self.tree.setIndexWidget(self._create_index_keywords(index_tuple), frame)

        self.tree.expandAll()

    def _create_index_keywords(self, index_tuple, pos=0, parent=QModelIndex()): #
        """
        Function to create the QModelIndex for the keyword column.
        Parameters
        ----------
        index_tuple : List[int]
            List of Index (from parent to child)
        pos : int
            current position in the index_tuple
        parent : QModelIndex()
            QModelIndex of the parent node.

        Returns
        -------
        QModelIndex()
            Index of the keyword field.
        """
        assert len(index_tuple) != 0, IndexError("index_tuple is empty")
        row = index_tuple[pos]
        pos_next = pos + 1

        if pos == 0:
            if len(index_tuple) == 1:
                return self.model.index(row, self.id_keywords)
            else:
                return self._create_index_keywords(index_tuple, pos=pos_next,
                                                   parent=self.model.index(row, 0))
        else:
            if pos_next < len(index_tuple):
                return self._create_index_keywords(index_tuple, pos=pos_next,
                                                   parent=self.model.index(row, 0, parent=parent))
            else:
                return self.model.index(row, self.id_keywords, parent=parent)


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