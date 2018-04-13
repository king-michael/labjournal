#!/usr/bin/env python
"""
# Details:
#   Frame for Information on TPR files inside the GROMACS entry
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

import os
import sys
from PyQt5 import QtWidgets
import pkg_resources

from labjournal.utils.regexHandler import reglob

from PyQt5.QtCore import QSettings

APPLICATION_NAME = 'foo'
COMPANY_NAME = 'foo'
settings = QSettings(APPLICATION_NAME, COMPANY_NAME)


class FrameTPR(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(FrameTPR, self).__init__(**kwargs)

        self.list_tprfiles = [] # empty list of tpr files
        # self.SIZE_widgetthermo = [300, 300]

        self.pattern_tprfile = str(settings.value('GROMACS/pattern/tprfile','.*.tpr'))

        for k,v in kwargs.iteritems():
            setattr(self,k,v)

        if not hasattr(self,'path'):
            if self.parent is None:
                self.path='.'
            else:
                self.path=self.parent.path

        # BEGIN TEST
        self.path=os.path.join(pkg_resources.resource_filename('labjournal', ''),'..',
                               "tests/test_folder_structures/dummy_andrej/dummy_folders/testcase_normalMD")

        # END TEST
        self.setupUI()

    def setupUI(self):
        """Create the Ui"""



        # set the layout
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)
        # Heading
        heading = QtWidgets.QLabel("TPR Files") # create heading
        layout_main.addWidget(heading) # register layout

        # layout_frame: horizontal line
        line_seperate = QtWidgets.QFrame()
        line_seperate.setMinimumSize(0, 0)
        line_seperate.setFrameShape(QtWidgets.QFrame.HLine)
        line_seperate.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout_main.addWidget(line_seperate)

        # frame
        self.layout_frame = QtWidgets.QHBoxLayout()
        layout_main.addLayout(self.layout_frame)

        # add vertical list
        # create tmp list with list and spacer
        layout_list_tmp = QtWidgets.QVBoxLayout()
        self.layout_frame.addLayout(layout_list_tmp)
        # list
        self.layout_list = QtWidgets.QVBoxLayout()
        layout_list_tmp.addLayout(self.layout_list)
        # spacer w ,h hPolicy, vPolicy
        spacerItem1 = QtWidgets.QSpacerItem(0, 0,
                                       QtWidgets.QSizePolicy.Expanding,
                                       QtWidgets.QSizePolicy.Maximum)
        layout_list_tmp.addItem(spacerItem1)

        self.display_tprfiles()

    def display_tprfiles(self):
        """display the list of tprfiles"""
        self.list_tprfiles = sorted(reglob(self.path, self.pattern_tprfile))
        for tpr in self.list_tprfiles:
            tpr_name = os.path.basename(tpr)
            label = QtWidgets.QLabel(tpr_name)
            self.layout_list.addWidget(label)

        # # normal ones
        # self.list_logfiles.extend(self.display_logfiles_per_location(None))
        #
        # # EM_and_Equilibration
        # self.list_logfiles.extend(
        #     self.display_logfiles_per_location(
        #         str(settings.value('LAMMPS/folders/EM_and_Equilibration', 'EM_and_Equilibration'))
        #     )
        # )
        # # production
        # self.list_logfiles.extend(
        #     self.display_logfiles_per_location(
        #         str(settings.value('LAMMPS/folders/production', 'production'))
        #     )
        # )
        # # add spacer at the end
        # spacerItem1 = QtWidgets.QSpacerItem(0, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        # self.layout_list.addItem(spacerItem1)

if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../../..')))  # add module to path
    app = QtWidgets.QApplication(sys.argv)
    window = FrameTPR(parent=None)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())