
# generate Uitest.py
#  pyuic4 test.ui -o Uitest.py

import sys
from PyQt4 import QtGui,QtCore

from Uitest import Ui_MainWindow

class GUi_MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,**kwargs):
        super(GUi_MainWindow,self).__init__(**kwargs)

        self.setupUi(self)
        self._init_menubar()

    def _init_menubar(self):

        # get the menuBar
        mainMenu = self.menuBar()
        # create a entry
        fileMenu = mainMenu.addMenu('&File')
        # create an action
        extractAction = QtGui.QAction("&LEAVE", self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        # add the action to fileMenu
        fileMenu.addAction(extractAction)

        databaseMenu = mainMenu.addMenu('&Database')
        # create an action
        extractAction = QtGui.QAction("&LEAVE", self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('Leave the app')
        extractAction.triggered.connect(self.close_application)
        # add the action to fileMenu
        databaseMenu.addAction(extractAction)

    def close_application(self):
        print("bye")
        sys.exit()


# TEST CASE
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GUi_MainWindow()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())

