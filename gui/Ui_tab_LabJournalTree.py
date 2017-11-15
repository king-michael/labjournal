# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UiWidgetLabjournalTree.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1129, 1181)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeWidget = QtGui.QTreeWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.header().setHighlightSections(True)
        self.gridLayout.addWidget(self.treeWidget, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditFilter = QtGui.QLineEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFilter.sizePolicy().hasHeightForWidth())
        self.lineEditFilter.setSizePolicy(sizePolicy)
        self.lineEditFilter.setObjectName(_fromUtf8("lineEditFilter"))
        self.horizontalLayout.addWidget(self.lineEditFilter)
        self.MainBtnRefreshFilter = QtGui.QCommandLinkButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainBtnRefreshFilter.sizePolicy().hasHeightForWidth())
        self.MainBtnRefreshFilter.setSizePolicy(sizePolicy)
        self.MainBtnRefreshFilter.setMaximumSize(QtCore.QSize(40, 16777215))
        self.MainBtnRefreshFilter.setText(_fromUtf8(""))
        self.MainBtnRefreshFilter.setObjectName(_fromUtf8("MainBtnRefreshFilter"))
        self.horizontalLayout.addWidget(self.MainBtnRefreshFilter)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.headerItem().setText(0, _translate("Form", "ID", None))
        self.treeWidget.headerItem().setText(1, _translate("Form", "MEDIAWIKI", None))
        self.treeWidget.headerItem().setText(2, _translate("Form", "New Column", None))
        self.treeWidget.headerItem().setText(3, _translate("Form", "Where", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "31", None))
        self.treeWidget.topLevelItem(0).setText(1, _translate("Form", "23", None))
        self.treeWidget.topLevelItem(0).setText(2, _translate("Form", "123", None))
        self.treeWidget.topLevelItem(0).setText(3, _translate("Form", "123", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Form", "New Subitem", None))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Form", " Subitem", None))
        self.treeWidget.topLevelItem(0).child(1).setText(1, _translate("Form", "213", None))
        self.treeWidget.topLevelItem(0).child(1).setText(2, _translate("Form", "3213", None))
        self.treeWidget.topLevelItem(0).child(1).setText(3, _translate("Form", "123", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "0", None))
        self.treeWidget.topLevelItem(1).setText(1, _translate("Form", "1", None))
        self.treeWidget.topLevelItem(1).setText(2, _translate("Form", "2", None))
        self.treeWidget.topLevelItem(1).setText(3, _translate("Form", "2", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.lineEditFilter.setText(_translate("Form", "Filter", None))

