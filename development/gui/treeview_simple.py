from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QTreeView,
                             QAbstractItemView)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

import sys


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


        for i in range(3):
            parent = QStandardItem(str(i))
            parent.setFlags(Qt.NoItemFlags) # not editable

            child1 = QStandardItem("->")
            child1.setFlags(Qt.NoItemFlags) # not editable
            child2 = QStandardItem(str(i*i))

            parent.appendRow([child1, child2])
            self.tree.model().appendRow(parent)

        self.tree.expandAll()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeView()
    treeWidgetDialog.show()
    sys.exit(app.exec_())