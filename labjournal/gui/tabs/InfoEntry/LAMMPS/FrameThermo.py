from __future__ import print_function

import os
import sys
import pkg_resources
from PyQt5 import QtCore, QtWidgets
from functools import partial

sys.path.insert(0,'../../../../../')  # Fixme: do we need this here?
ROOT = os.path.realpath(pkg_resources.resource_filename('labjournal',''))
# FIXME do we need InfoEntry here?
try:
    from ..InfoEntry import InfoEntry  # Fixme: get rid of of relative imports
except: # so we can use it as module and right as script...
    sys.path.insert(0, "../..")
    from InfoEntry import InfoEntry

from WidgetThermo import WidgetThermo
from labjournal.utils.regexHandler import reglob

from PyQt5.QtCore import QSettings
settings = QSettings('foo', 'foo')

class FrameThermo(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(FrameThermo, self).__init__(**kwargs)

        self.list_logfiles = [] # empty list of logfiles
        self.SIZE_widgetthermo = [300, 300]

        self.pattern_logfile = str(settings.value('LAMMPS/pattern/logfile','log..*.lammps'))

        for k,v in kwargs.iteritems():
            setattr(self,k,v)

        if not hasattr(self,'path'):
            if self.parent is None:
                self.path='.'
            else:
                self.path=self.parent.path

        # BEGIN TEST
        self.path =os.path.join(ROOT, "../tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD")
        # END TEST
        self.setupUI()

    def setupUI(self):
        """Create the Ui"""



        # set the layout
        layout_main = QtWidgets.QVBoxLayout()
        self.setLayout(layout_main)
        # Heading
        heading = QtWidgets.QLabel("Thermo") # create heading
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

        self.display_logfiles()
        if len(self.list_logfiles) >0:
            self.update_widgetthermo(self.list_logfiles[0])

    def update_widgetthermo(self,logfile=None):
        if hasattr(self,"widgetthermo"):
            self.layout_frame.removeWidget(self.widgetthermo)
        if logfile is None:
            return
        else:
            self.widgetthermo = WidgetThermo(logfile=logfile,
                                             SIZE=self.SIZE_widgetthermo,
                                             OPTION_TOOLBAR=False,
                                             OPTION_LEGEND=True)
            self.widgetthermo.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
            self.widgetthermo.canvas.setMinimumSize(*self.SIZE_widgetthermo)
            self.widgetthermo.canvas.setMaximumSize(*self.SIZE_widgetthermo)
            self.widgetthermo.canvas.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        self.layout_frame.addWidget(self.widgetthermo)

    def logfile_clicked(self,logfile):
        """Action when the logfile button is clicked"""
        self.update_widgetthermo(logfile)

    def create_item(self,text):
        """create a logfile item"""
        item = QtWidgets.QToolButton(self)
        item.setText(text)
        font = item.font()
        font.setBold(True)
        item.setFont(font)
        item.setStyleSheet("""
                                background-color: #00a9e0;
                                color: rgb(255, 255, 255);
                                border: 0 px;
                                border-radius: 15;
                                """)
        return item

    def display_logfiles_per_location(self,location=None):
        """Find and display the logfiles for a given locations"""
        if location is None:
            logfiles = sorted(reglob(self.path, self.pattern_logfile))
        else:
            path=os.path.join(self.path, location)
            if os.path.exists(path):
                logfiles = sorted(reglob(path, self.pattern_logfile))
            else:
                return []
        if location is not None and len(logfiles) > 0:
            label = QtWidgets.QLabel(location)
            self.layout_list.addWidget(label)

        for logfile in logfiles:
            fname = os.path.basename(logfile)
            item=self.create_item(fname)
            item.clicked.connect(partial(self.logfile_clicked, logfile))
            self.layout_list.addWidget(item)
        return logfiles

    def display_logfiles(self):
        """display the list of logfiles"""
        # normal ones
        self.list_logfiles.extend(self.display_logfiles_per_location(None))
        # EM_and_Equilibration
        self.list_logfiles.extend(
            self.display_logfiles_per_location(
                str(settings.value('LAMMPS/folders/EM_and_Equilibration', 'EM_and_Equilibration'))
            )
        )
        # production
        self.list_logfiles.extend(
            self.display_logfiles_per_location(
                str(settings.value('LAMMPS/folders/production', 'production'))
            )
        )
        # add spacer at the end
        spacerItem1 = QtWidgets.QSpacerItem(0, 300, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.layout_list.addItem(spacerItem1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FrameThermo(parent=None)

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())