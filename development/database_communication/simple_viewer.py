"""
Simple viewer for the Main table of the database.
Directly connected to the simdb interface.
"""

from __future__ import absolute_import

from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLineEdit,
                             QPushButton,
                             QFileDialog,
                             QTableView)

from simdb.databaseAPI import getEntryTable

from PandasModel import PandasModel

# Answer to: https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5
# Copied from: https://github.com/eyllanesc/stackoverflow/tree/master/PandasTableView
# modified to work with our database


class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        vLayout = QVBoxLayout(self)
        hLayout = QHBoxLayout()
        self.pathLE = QLineEdit(self)
        hLayout.addWidget(self.pathLE)
        self.loadBtn = QPushButton("Select File", self)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.pandasTv = QTableView(self)
        vLayout.addWidget(self.pandasTv)
        self.loadBtn.clicked.connect(self.loadFile)
        self.pandasTv.setSortingEnabled(True)

    def loadFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "database files (*.db)");
        self.pathLE.setText(fileName)
        table = getEntryTable(fileName,
                              columns=["entry_id",
                                       "path",
                                       "created_on",
                                       "added_on",
                                       "updated_on",
                                       "description"],
                              load_keys=False,
                              load_tags=False,
                              )
        model = PandasModel(table)
        self.pandasTv.setModel(model)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())