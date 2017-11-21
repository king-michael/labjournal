# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1444, 896)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frameSide = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameSide.sizePolicy().hasHeightForWidth())
        self.frameSide.setSizePolicy(sizePolicy)
        self.frameSide.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameSide.setFrameShadow(QtGui.QFrame.Raised)
        self.frameSide.setObjectName(_fromUtf8("frameSide"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frameSide)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        spacerItem = QtGui.QSpacerItem(400, 10, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 8, 0, 1, 1)
        self.line = QtGui.QFrame(self.frameSide)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_5.addWidget(self.line, 3, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.frameSide)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_5.addWidget(self.pushButton_3, 6, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.frameSide)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_5.addWidget(self.pushButton, 4, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.frameSide)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_5.addWidget(self.pushButton_2, 5, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 7, 0, 1, 1)
        self.widget = QtGui.QWidget(self.frameSide)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.MySearch_lineEdit = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MySearch_lineEdit.sizePolicy().hasHeightForWidth())
        self.MySearch_lineEdit.setSizePolicy(sizePolicy)
        self.MySearch_lineEdit.setObjectName(_fromUtf8("MySearch_lineEdit"))
        self.horizontalLayout.addWidget(self.MySearch_lineEdit)
        self.MySearch_pushButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MySearch_pushButton.sizePolicy().hasHeightForWidth())
        self.MySearch_pushButton.setSizePolicy(sizePolicy)
        self.MySearch_pushButton.setObjectName(_fromUtf8("MySearch_pushButton"))
        self.horizontalLayout.addWidget(self.MySearch_pushButton)
        self.gridLayout_5.addWidget(self.widget, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frameSide)
        self.frameMain = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameMain.sizePolicy().hasHeightForWidth())
        self.frameMain.setSizePolicy(sizePolicy)
        self.frameMain.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameMain.setFrameShadow(QtGui.QFrame.Raised)
        self.frameMain.setObjectName(_fromUtf8("frameMain"))
        self.gridLayout = QtGui.QGridLayout(self.frameMain)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.frameMain)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.MyTabLabJournalIndex = QtGui.QWidget()
        self.MyTabLabJournalIndex.setObjectName(_fromUtf8("MyTabLabJournalIndex"))
        self.verticalLayout = QtGui.QVBoxLayout(self.MyTabLabJournalIndex)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget.addTab(self.MyTabLabJournalIndex, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.frameMain)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1444, 28))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.MySearch_lineEdit.setText(_translate("MainWindow", "Search (goto)", None))
        self.MySearch_pushButton.setText(_translate("MainWindow", "Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MyTabLabJournalIndex), _translate("MainWindow", "Overview", None))

