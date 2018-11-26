from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QFrame,
                             QVBoxLayout, QHBoxLayout,
                             QLabel, QToolButton,
                             QTreeView,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, QModelIndex

from simdb.databaseModel import Keywords, Main, create_engine, sessionmaker
import sys

class KeywordLabel(QLabel):
    def __init__(self,keyword='', value=None, parent=None):
        super(QLabel, self).__init__(parent)

        stylesheet = " ".join([
            'border-radius: 10px;',
            'background-color: #00a9e0;',
            'color: white;'
        ])
        self.setStyleSheet(stylesheet)

        self.setMinimumSize(QSize(40, 40))
        self.setAlignment(Qt.AlignCenter)

        font_size_big = 12
        font_size_small = 8
        # set text
        if value is None or value == 'None':
            text = "<span style='font-size:{}pt; font-weight:600;'>{}</span>".format(font_size_big, keyword)
        else:
            text = "<span style='font-size:{}pt; font-weight:600;'>{}</span><br>".format(font_size_small, keyword)
            text += "<span style='font-size:{}pt; font-weight:600;'>{}</span>".format(font_size_big, value)
        self.setText(text)


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
        frame.setLayout(QHBoxLayout())
        for i, keyword in enumerate(keywords):
            label = KeywordLabel(keyword=keyword.name, value=keyword.value)
            frame.layout().addWidget(label)
        return frame

    def _create_row(self, i, sim):

        list_keywords = []

        # build row
        list_row = [QStandardItem(str(getattr(sim, attr) if attr != 'keywords' else ''))
                    for attr in self.header]

        # set parent attributes
        for parent in list_row:
            parent.setFlags(Qt.NoItemFlags)

        # add keywords
        if self.id_keywords is not None and len(sim.keywords) != 0:
            list_keywords.append([(i, None), sim.keywords])

        # add children
        if self.nested_mode and len(sim.children) > 0:
            for j, child in enumerate(sorted(sim.children, key=lambda x: x.child.entry_id)):
                child_row, _ = self._create_row(j, child.child)
                list_keywords.append([(j, i), child.child.keywords])

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

        self.id_keywords = self.header.index('keywords') if 'keywords' in self.header else None
        list_keywords = []

        if self.nested_mode:
            sims = session.query(Main).join().filter(~Main.parents.any()).order_by(Main.entry_id).all()
        else:
            sims = session.query(Main).order_by(Main.entry_id).all()

        for i, sim in enumerate(sims):
            list_row, sublist_keywords = self._create_row(i, sim)
            list_keywords.extend(sublist_keywords)
            self.model.appendRow(list_row)


        for (i, parent), keywords in list_keywords:
            frame = self._create_keywords_labels(keywords=keywords)
            if parent is not None:
                self.tree.setIndexWidget(self.model.index(i, ))
            else:
                self.tree.setIndexWidget(self.model.index(i, self.id_keywords), frame)

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

        # for i in range(4):
        #     parent = QStandardItem(str(i))
        #     parent.setFlags(Qt.NoItemFlags) # not editable
        #
        #     child1 = QStandardItem("->")
        #     child1.setFlags(Qt.NoItemFlags) # not editable
        #     child2 = QStandardItem(str(i*i))
        #
        #     parent.appendRow([child1, child2])
        #     self.tree.model().appendRow(parent)
        #
        # label = QLabel("A test")
        # label.setStyleSheet('background : red;')
        # self.tree.setIndexWidget( self.tree.model().index(0,1), label)
        #
        # label = QLabel("A new test")
        # label.setStyleSheet('background : green;')
        # self.tree.setIndexWidget(self.tree.model().index(0, 1, parent=self.tree.model().index(1, 0)), label)
        #
        # frame = QFrame()
        # frame.setLayout(QHBoxLayout())
        # for i in range(3):
        #     label = QLabel("label : {}".format(i))
        #     label.setStyleSheet('background : blue;')
        #     frame.layout().addWidget(label)
        # self.tree.setIndexWidget(
        #     self.tree.model().index(0, 1,
        #                             parent=self.tree.model().index(3, 0)),
        #     frame)
        # self.tree.expandAll()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeView()
    treeWidgetDialog.show()
    sys.exit(app.exec_())