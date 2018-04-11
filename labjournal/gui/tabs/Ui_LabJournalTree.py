# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_LabJournalTree.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1129, 1181)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setHighlightSections(True)
        self.gridLayout.addWidget(self.treeWidget, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditFilter = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFilter.sizePolicy().hasHeightForWidth())
        self.lineEditFilter.setSizePolicy(sizePolicy)
        self.lineEditFilter.setText("")
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.horizontalLayout.addWidget(self.lineEditFilter)
        self.MainBtnRefreshFilter = QtWidgets.QCommandLinkButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MainBtnRefreshFilter.sizePolicy().hasHeightForWidth())
        self.MainBtnRefreshFilter.setSizePolicy(sizePolicy)
        self.MainBtnRefreshFilter.setMaximumSize(QtCore.QSize(40, 16777215))
        self.MainBtnRefreshFilter.setText("")
        self.MainBtnRefreshFilter.setObjectName("MainBtnRefreshFilter")
        self.horizontalLayout.addWidget(self.MainBtnRefreshFilter)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget.setSortingEnabled(True)
        self.lineEditFilter.setPlaceholderText(_translate("Form", "Filter"))

