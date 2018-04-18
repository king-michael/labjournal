"""
Widget to show details about the system
"""

import os
import pkg_resources
import logging

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from Ui_MDSystemOverview import Ui_Form
from pymolwidget import PyMolWidget
from glob import glob

logger = logging.getLogger('LabJournal')
os.environ["PYMOL_PATH"] = os.path.realpath(pkg_resources.resource_filename('pymol', ''))
from pymol import cmd as pm

class MDSystemOverview(QWidget,Ui_Form):
    def __init__(self, path, **kwargs):
        super(MDSystemOverview, self).__init__(**kwargs)
        self.setupUi(self)

        self.path = path # set path

        self.setup_variables()  # setup some variables


        self.setup_display()

    def setup_variables(self):
        list_pdbfiles = glob(os.path.join(self.path, '*.pdb'))
        if len(list_pdbfiles) == 0:
            self.pdb_file = None
        elif len(list_pdbfiles) == 1:
            self.pdb_file = os.path.basename(list_pdbfiles[0])
        else:
            self.pdb_file = [os.path.basename(f) for f in list_pdbfiles]
            raise NotImplementedError("Not implemented more then one pdb file")

    def setup_display(self):
        """
        Function to display the structure
        """
        if self.pdb_file is not None:
            # setup pymolWidget
            self.pymolWidget = PyMolWidget(self)  # start pymolwidget
            self.pymolWidget.setFixedWidth(400)  # set width
            self.pymolWidget.setFixedHeight(self.pymolWidget.width())  # make it squarewise
            self.layout_display.addWidget(self.pymolWidget)  #
            self.layout_displayside.addStretch(1)  # add a strech area below (so it will be at the top always)

            self.pymolWidget.loadMolFile(os.path.join(self.path,self.pdb_file))
        else: # Todo: Implement several pdb files if found
            return

if __name__ == '__main__':
    import sys


    #sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    path = os.path.join(os.path.realpath(pkg_resources.resource_filename('labjournal', ''))
                        , "../tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD")
    window = MDSystemOverview(path = path)

    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
