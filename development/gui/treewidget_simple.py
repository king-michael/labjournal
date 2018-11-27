from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QTreeWidget,
                             QTreeWidgetItem)
import sys


class SimpleTreeWidget(QWidget):
    def __init__(self):
        super(SimpleTreeWidget, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        # Creating the required widgets
        self.vboxLayout = QVBoxLayout()
        self.setLayout(self.vboxLayout)


        self.treeWidget = QTreeWidget()

        # Adding the widgets
        self.vboxLayout.addWidget(self.treeWidget)
        self.treeWidget.setHeaderLabel("TreeWidget oO")

        self.topLevelItem = QTreeWidgetItem(self.treeWidget)

        for i, header in enumerate(['x', 'x^2']):
            self.treeWidget.headerItem().setText(i, header)

        # Adding the child to the top level item
        self.childItems = []
        for i in range(4):
            child = QTreeWidgetItem(self.treeWidget)
            child.setText(0, str(i))
            child.setText(1, str(i*i))
            self.childItems.append(child)
            self.topLevelItem.addChild(child)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    treeWidgetDialog = SimpleTreeWidget()
    treeWidgetDialog.show()
    sys.exit(app.exec_())