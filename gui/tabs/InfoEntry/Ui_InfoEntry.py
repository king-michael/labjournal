# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_InfoEntry.ui'
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
        Form.resize(1191, 1453)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layout_header = QtGui.QVBoxLayout()
        self.layout_header.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.layout_header.setObjectName(_fromUtf8("layout_header"))
        self.label_infobox = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_infobox.sizePolicy().hasHeightForWidth())
        self.label_infobox.setSizePolicy(sizePolicy)
        self.label_infobox.setObjectName(_fromUtf8("label_infobox"))
        self.layout_header.addWidget(self.label_infobox)
        self.layout_generalinfo = QtGui.QHBoxLayout()
        self.layout_generalinfo.setObjectName(_fromUtf8("layout_generalinfo"))
        self.frame_generalInfo = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_generalInfo.sizePolicy().hasHeightForWidth())
        self.frame_generalInfo.setSizePolicy(sizePolicy)
        self.frame_generalInfo.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_generalInfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_generalInfo.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_generalInfo.setObjectName(_fromUtf8("frame_generalInfo"))
        self.label_infobox.raise_()
        self.layout_generalinfo.addWidget(self.frame_generalInfo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout_generalinfo.addItem(spacerItem)
        self.layout_header.addLayout(self.layout_generalinfo)
        self.layout_box_tags = QtGui.QHBoxLayout()
        self.layout_box_tags.setObjectName(_fromUtf8("layout_box_tags"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.layout_box_tags.addWidget(self.label)
        self.layout_tags = QtGui.QGridLayout()
        self.layout_tags.setObjectName(_fromUtf8("layout_tags"))
        self.layout_box_tags.addLayout(self.layout_tags)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout_box_tags.addItem(spacerItem1)
        self.layout_header.addLayout(self.layout_box_tags)
        self.verticalLayout.addLayout(self.layout_header)
        self.line_seperate = QtGui.QFrame(Form)
        self.line_seperate.setFrameShape(QtGui.QFrame.HLine)
        self.line_seperate.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_seperate.setObjectName(_fromUtf8("line_seperate"))
        self.verticalLayout.addWidget(self.line_seperate)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem2 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.layout_body = QtGui.QVBoxLayout()
        self.layout_body.setObjectName(_fromUtf8("layout_body"))
        self.gridLayout.addLayout(self.layout_body, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_infobox.setText(_translate("Form", "General Informations", None))
        self.label.setText(_translate("Form", "tags", None))

