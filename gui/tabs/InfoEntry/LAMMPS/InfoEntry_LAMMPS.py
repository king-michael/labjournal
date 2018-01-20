#!/usr/bin/env python
"""
# Details:
#   Wrapper around InfoEntry for LAMMPS
# Authors:
#   Michael King <michael.king@uni-konstanz.de>
# History:
#   -
# Last modified: 21.10.2017
# ToDo:
#   -
# Bugs:
#   -
"""

from __future__ import print_function

import sys,os
from PyQt4 import QtCore, QtGui

root = "../../../.."
sys.path.insert(0,root)

try:
    from ..InfoEntry import InfoEntry
except: # so we can use it as module and right as script...
    sys.path.insert(0, "../..")
    from InfoEntry import InfoEntry

from FrameThermo import FrameThermo

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


class InfoEntry_LAMMPS(InfoEntry):
    def __init__(self,**kwargs):
        super(InfoEntry_LAMMPS,self).__init__(**kwargs)
        print("DAS")

        # TEST
        self.path=os.path.join("/home/micha/SIM-PhD-King/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/production")
        self.disguise()
    def disguise(self):
        """apply LAMMPS disguise"""

        #btn = QtGui.QPushButton("Open Thermo Data")
        #btn.clicked.connect(self.PopUp_WidgetThermo)
        self.FrameThermo = FrameThermo(parent=self)
        self.layout_body.addWidget(self.FrameThermo)

        spacerItem1 = QtGui.QSpacerItem(10, 10,
                                   QtGui.QSizePolicy.MinimumExpanding,
                                   QtGui.QSizePolicy.MinimumExpanding)
        self.layout_body.addItem(spacerItem1)
    def PopUp_WidgetThermo(self):
        widgetthermo = WidgetThermo(path=self.path)
        widgetthermo.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = InfoEntry_LAMMPS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())
