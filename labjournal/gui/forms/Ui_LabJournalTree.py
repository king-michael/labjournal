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
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setContentsMargins(9, 9, -1, -1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLineEdit = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchLineEdit.sizePolicy().hasHeightForWidth())
        self.searchLineEdit.setSizePolicy(sizePolicy)
        self.searchLineEdit.setText("")
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout.addWidget(self.searchLineEdit)
        self.searchButton = QtWidgets.QCommandLinkButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.searchButton.setText("")
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.widgetOptions = QtWidgets.QWidget(Form)
        self.widgetOptions.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetOptions.sizePolicy().hasHeightForWidth())
        self.widgetOptions.setSizePolicy(sizePolicy)
        self.widgetOptions.setObjectName("widgetOptions")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widgetOptions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.optionShowOptions = QtWidgets.QRadioButton(self.widgetOptions)
        self.optionShowOptions.setAutoExclusive(False)
        self.optionShowOptions.setObjectName("optionShowOptions")
        self.verticalLayout.addWidget(self.optionShowOptions)
        self.frameOptions = QtWidgets.QFrame(self.widgetOptions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameOptions.sizePolicy().hasHeightForWidth())
        self.frameOptions.setSizePolicy(sizePolicy)
        self.frameOptions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOptions.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameOptions.setObjectName("frameOptions")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameOptions)
        self.verticalLayout_3.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.optionParentView = QtWidgets.QRadioButton(self.frameOptions)
        self.optionParentView.setEnabled(True)
        self.optionParentView.setObjectName("optionParentView")
        self.verticalLayout_3.addWidget(self.optionParentView)
        self.optionShowOptions.raise_()
        self.optionParentView.raise_()
        self.verticalLayout.addWidget(self.frameOptions, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_4.addWidget(self.widgetOptions)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.searchLineEdit.setPlaceholderText(_translate("Form", "Filter"))
        self.optionShowOptions.setText(_translate("Form", "show options"))
        self.optionParentView.setText(_translate("Form", "toggle parent view"))

