#!/usr/bin/env python
"""
# Details:
#   Wrapper around UiInfoEntry_LAMMPS.py
# Authors:
#   Michael King <michael.king@uni-konstanz.de>
# History:
#   -
# Last modified: 17.10.2017
# ToDo:
#   -
# Bugs:
#   -
"""

from __future__ import print_function
from PyQt4 import QtCore, QtGui
import sys

from Ui_tab_InfoEntry_LAMMPS import Ui_Form

# import webbrowser

sys.path.append("..")
from Ui_tab_InfoEntry  import Ui_Form
from GUi_tab_InfoEntry import *

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


class GUi_tab_InfoEntry_LAMMPS(GUi_tab_InfoEntry):
    def __init__(self,**kwargs):
        super(self.__class__,self).__init__(**kwargs)
        print("YEAH")



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = GUi_tab_InfoEntry_LAMMPS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
