#!/usr/bin/env python
"""
# Details:
#   Wrapper around InfoEntry for GROMACS simulations
# Authors:
#   Andrej Berg
# History:
#   -
# Last modified: 09.04.2018
# ToDo:
#   -
# Bugs:
#   -
"""

from __future__ import print_function

import sys,os
from PyQt5 import QtWidgets

from labjournal.gui.tabs.InfoEntry import InfoEntry
from labjournal.gui.tabs.InfoEntry.general.MDSystemOverview import MDSystemOverview

class InfoEntry_GROMACS(InfoEntry):
    def __init__(self,**kwargs):
        super(InfoEntry_GROMACS,self).__init__(**kwargs)

        self.disguise()

    def disguise(self):
        """apply disguise"""

        self.FrameMDSystemOverview = MDSystemOverview(path=self.path)
        self.layout_body.addWidget(self.FrameMDSystemOverview)

        # <<<<<< CHANGE HERE
        # adding Example Widget in layout body
        #self.ExampleWidget = SomeExampleWidget(parent=self)
        #self.layout_body.addWidget(self.ExampleWidget)
        # <<<<<< CHANGE HERE



        # Should be last and not changed / adding space at the bottom
        spacerItem1 = QtWidgets.QSpacerItem(10, 10,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                   QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout_body.addItem(spacerItem1)

    def do_stupid_custom_stuff(self):
        """
        arbitrary custom function
        """


if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../..')))  # add module to path

    app = QtWidgets.QApplication(sys.argv)
    window = InfoEntry_GROMACS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
