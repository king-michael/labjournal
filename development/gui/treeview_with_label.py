from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QFrame,
                             QVBoxLayout, QHBoxLayout,
                             QLabel,
                             QTreeView,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, QModelIndex

import sys

class KeywordLabel(QLabel):
    def __init__(self,keyword='', value=None, parent=None):
        super(QLabel, self).__init__(parent)

        stylesheet = " ".join([
            'border-radius: 10px;',
            'background: rgb(170, 170, 255);',
            'color: white;'
        ])
        self.setStyleSheet(stylesheet)

        self.setMinimumSize(QSize(40, 40))
        self.setAlignment(Qt.AlignCenter)

        # set text
        if value is None:
            text = "<span style='font-size:18pt; font-weight:600;'>{}</span>".format(keyword)
        else:
            text = "<span style='font-size:10pt; font-weight:600;'>{}</span><br>".format(keyword)
            text += "<span style='font-size:18pt; font-weight:600;'>{}</span>".format(value)
        self.setText(text)


class SimpleTreeView(QWidget):
    def __init__(self):
        super(SimpleTreeView, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)

        # Tree view
        self.tree = QTreeView()
        self.vboxLayout.addWidget(self.tree)

        self.tree.setModel(QStandardItemModel())
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(True)
        self.tree.setHeaderHidden(False)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectItems)

        self.tree.model().setHorizontalHeaderLabels(['Parameter', 'Value'])


        for i in range(4):
            parent = QStandardItem(str(i))
            parent.setFlags(Qt.NoItemFlags) # not editable

            child1 = QStandardItem("->")
            child1.setFlags(Qt.NoItemFlags) # not editable
            child2 = QStandardItem(str(i*i))

            parent.appendRow([child1, child2])
            self.tree.model().appendRow(parent)

        # child of child
        i += 1
        parent = QStandardItem(str(i))
        parent.setFlags(Qt.NoItemFlags)  # not editable

        child1 = QStandardItem("->")
        child1.setFlags(Qt.NoItemFlags)  # not editable
        child2 = QStandardItem(str(i * i))

        child1_sub = QStandardItem("+++")
        child1_sub.setFlags(Qt.NoItemFlags)  # not editable
        child2_sub = QStandardItem('')
        child1.appendRow([child1_sub, child2_sub])
        parent.appendRow([child1, child2])
        self.tree.model().appendRow(parent)

        label = QLabel("A test")
        label.setStyleSheet('background : red;')
        self.tree.setIndexWidget( self.tree.model().index(0,1, parent=QModelIndex()), label)

        label = QLabel("other test")
        label.setStyleSheet('background : yellow;')
        self.tree.setIndexWidget(self.tree.model().index(2, 1, parent=QModelIndex()), label)

        label = QLabel("A new test")
        label.setStyleSheet('background : green;')
        self.tree.setIndexWidget(self.tree.model().index(0, 1, parent=self.tree.model().index(1, 0)), label)


        label = QLabel("A")
        label.setStyleSheet('background:lightblue')
        self.tree.setIndexWidget(self.tree.model().index(0,1, parent=self.tree.model().index(0,0, parent=self.tree.model().index(4, 0))),
                                 label)

        frame = QFrame()
        frame.setLayout(QHBoxLayout())
        for i in range(3):
            label = QLabel("label : {}".format(i))
            label.setStyleSheet('background : blue;')
            frame.layout().addWidget(label)
        self.tree.setIndexWidget(
            self.tree.model().index(0, 1,
                                    parent=self.tree.model().index(3, 0)),
            frame)


        self.tree.expandAll()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeView()
    treeWidgetDialog.show()
    sys.exit(app.exec_())