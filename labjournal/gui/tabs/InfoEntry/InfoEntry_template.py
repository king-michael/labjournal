#!/usr/bin/env python
"""
# Details:
#   Template for wrapper around InfoEntry
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


class InfoEntry_LAMMPS(InfoEntry):
    def __init__(self,**kwargs):
        super(InfoEntry_LAMMPS,self).__init__(**kwargs)

        self.disguise()

    def disguise(self):
        """apply disguise"""

        # <<<<<< CHANGE HERE
        # adding Example Widget in layout body
        self.ExampleWidget = SomeExampleWidget(parent=self)
        self.layout_body.addWidget(self.ExampleWidget)
        # <<<<<< CHANGE HERE


        # Should be last and not changed / adding space at the bottom
        spacerItem1 = QtGui.QSpacerItem(10, 10,
                                   QtGui.QSizePolicy.MinimumExpanding,
                                   QtGui.QSizePolicy.MinimumExpanding)
        self.layout_body.addItem(spacerItem1)

    def do_stupid_custom_stuff(self):
        """
        arbitrary custom function
        """


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
