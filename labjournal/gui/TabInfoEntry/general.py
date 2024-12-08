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

import logging

from PyQt5.QtWidgets import (QApplication,
                             QWidget,)

from labjournal.gui.forms.Ui_TabInfoEntry import Ui_Form
from simdb.databaseAPI import get_entry_details

logger = logging.getLogger('LabJournal.TabInfoEntry')

class InfoEntry(QWidget, Ui_Form):
    def __init__(self, main_id, parent=None):

        super(InfoEntry, self).__init__(parent)

        # set defaults
        self.parent = None
        self.main_id = main_id

        # EXPERIMENTAL
        db_path = '../micha_raw.db'

        details = get_entry_details(db_path)


if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    window = InfoEntry(main_id = 1)

    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
