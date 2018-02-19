# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_DialogNewEntry.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(546, 493)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_simid = QtGui.QLineEdit(Dialog)
        self.lineEdit_simid.setObjectName(_fromUtf8("lineEdit_simid"))
        self.horizontalLayout.addWidget(self.lineEdit_simid)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_mediawiki = QtGui.QLineEdit(Dialog)
        self.lineEdit_mediawiki.setObjectName(_fromUtf8("lineEdit_mediawiki"))
        self.horizontalLayout.addWidget(self.lineEdit_mediawiki)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_path = QtGui.QLineEdit(Dialog)
        self.lineEdit_path.setObjectName(_fromUtf8("lineEdit_path"))
        self.horizontalLayout_2.addWidget(self.lineEdit_path)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.textEdit_description = QtGui.QTextEdit(Dialog)
        self.textEdit_description.setObjectName(_fromUtf8("textEdit_description"))
        self.verticalLayout.addWidget(self.textEdit_description)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.textEdit_tags = QtGui.QTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_tags.sizePolicy().hasHeightForWidth())
        self.textEdit_tags.setSizePolicy(sizePolicy)
        self.textEdit_tags.setObjectName(_fromUtf8("textEdit_tags"))
        self.verticalLayout.addWidget(self.textEdit_tags)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lineEdit_simtype = QtGui.QLineEdit(Dialog)
        self.lineEdit_simtype.setObjectName(_fromUtf8("lineEdit_simtype"))
        self.horizontalLayout_3.addWidget(self.lineEdit_simtype)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 9, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEdit_simid, self.lineEdit_mediawiki)
        Dialog.setTabOrder(self.lineEdit_mediawiki, self.lineEdit_path)
        Dialog.setTabOrder(self.lineEdit_path, self.textEdit_description)
        Dialog.setTabOrder(self.textEdit_description, self.textEdit_tags)
        Dialog.setTabOrder(self.textEdit_tags, self.lineEdit_simtype)
        Dialog.setTabOrder(self.lineEdit_simtype, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create new Database Entry", None))
        self.label.setText(_translate("Dialog", "Simid:", None))
        self.label_2.setText(_translate("Dialog", "MediaWiki", None))
        self.label_3.setText(_translate("Dialog", "Path:", None))
        self.label_4.setText(_translate("Dialog", "Description:", None))
        self.label_5.setText(_translate("Dialog", "Tags & Keywords:", None))
        self.label_6.setText(_translate("Dialog", "Simtype:", None))

