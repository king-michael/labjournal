# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_InfoEntry.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1191, 1453)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_header = QtWidgets.QVBoxLayout()
        self.layout_header.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout_header.setObjectName("layout_header")
        self.label_infobox = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_infobox.sizePolicy().hasHeightForWidth())
        self.label_infobox.setSizePolicy(sizePolicy)
        self.label_infobox.setObjectName("label_infobox")
        self.layout_header.addWidget(self.label_infobox)
        self.layout_generalinfo = QtWidgets.QHBoxLayout()
        self.layout_generalinfo.setObjectName("layout_generalinfo")
        self.frame_generalInfo = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_generalInfo.sizePolicy().hasHeightForWidth())
        self.frame_generalInfo.setSizePolicy(sizePolicy)
        self.frame_generalInfo.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_generalInfo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_generalInfo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_generalInfo.setObjectName("frame_generalInfo")
        self.layout_generalinfo.addWidget(self.frame_generalInfo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_generalinfo.addItem(spacerItem)
        self.layout_header.addLayout(self.layout_generalinfo)
        self.layout_tags_keywords = QtWidgets.QGridLayout()
        self.layout_tags_keywords.setObjectName("layout_tags_keywords")
        self.label_keywords = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_keywords.sizePolicy().hasHeightForWidth())
        self.label_keywords.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_keywords.setFont(font)
        self.label_keywords.setWordWrap(False)
        self.label_keywords.setObjectName("label_keywords")
        self.layout_tags_keywords.addWidget(self.label_keywords, 1, 0, 1, 1)
        self.label_tags = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_tags.sizePolicy().hasHeightForWidth())
        self.label_tags.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_tags.setFont(font)
        self.label_tags.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_tags.setTextFormat(QtCore.Qt.PlainText)
        self.label_tags.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_tags.setObjectName("label_tags")
        self.layout_tags_keywords.addWidget(self.label_tags, 0, 0, 1, 1)
        self.layout_header.addLayout(self.layout_tags_keywords)
        self.verticalLayout.addLayout(self.layout_header)
        self.line_seperate = QtWidgets.QFrame(Form)
        self.line_seperate.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_seperate.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_seperate.setObjectName("line_seperate")
        self.verticalLayout.addWidget(self.line_seperate)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.layout_body = QtWidgets.QVBoxLayout()
        self.layout_body.setObjectName("layout_body")
        self.gridLayout.addLayout(self.layout_body, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_infobox.setText(_translate("Form", "General Informations"))
        self.label_keywords.setText(_translate("Form", "keywords:"))
        self.label_tags.setText(_translate("Form", "tags:"))

