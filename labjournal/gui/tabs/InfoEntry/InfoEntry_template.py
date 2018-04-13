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

import sys
import os
import logging

from PyQt5 import QtWidgets
# if __name__ == '__main__':
#     sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..')))  # add module to path

from labjournal.gui.tabs.InfoEntry import InfoEntry

logger = logging.getLogger('LabJournal')


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
        spacerItem1 = QtWidgets.QSpacerItem(10, 10,
                                   QtWidgets.QSizePolicy.MinimumExpanding,
                                   QtWidgets.QSizePolicy.MinimumExpanding)
        self.layout_body.addItem(spacerItem1)

    def do_stupid_custom_stuff(self):
        """
        arbitrary custom function
        """


if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)

    app = QtWidgets.QApplication(sys.argv)
    window = InfoEntry_LAMMPS(ID=2)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
