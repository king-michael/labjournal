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
from PyQt5 import QtWidgets

from old_labjournal.gui.tabs.InfoEntry import InfoEntry
from old_labjournal.gui.tabs.InfoEntry.general.MDSystemOverview import MDSystemOverview
from FrameThermo import FrameThermo

class InfoEntry_LAMMPS(InfoEntry):
    def __init__(self,**kwargs):
        super(InfoEntry_LAMMPS,self).__init__(**kwargs)

        # TEST
        self.path=os.path.join("/home/micha/SIM-PhD-King/old_labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD")
        self.disguise()

    def disguise(self):
        """apply LAMMPS disguise"""

        self.FrameMDSystemOverview = MDSystemOverview(path = self.path)
        self.layout_body.addWidget(self.FrameMDSystemOverview)

        #btn = QtWidgets.QPushButton("Open Thermo Data")
        #btn.clicked.connect(self.PopUp_WidgetThermo)
        self.FrameThermo = FrameThermo(parent=self)
        self.layout_body.addWidget(self.FrameThermo)

        spacerItem1 = QtWidgets.QSpacerItem(10, 10,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                   QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout_body.addItem(spacerItem1)
    def PopUp_WidgetThermo(self):
        widgetthermo = WidgetThermo(path=self.path)
        widgetthermo.show()


if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../..')))  # add module to path
    app = QtWidgets.QApplication(sys.argv)
    window = InfoEntry_LAMMPS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
