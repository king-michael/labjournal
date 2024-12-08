"""
Widget to show details about the system
"""

import os
import pkg_resources
import logging
import MDAnalysis

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
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

        # add a pushButton to show the structure
        self.pushButtonShow = QPushButton("show structure")
        self.pushButtonShow.pressed.connect(self.event_press_show)
        self.layout_display.addWidget(self.pushButtonShow)
        #self.setup_display()

        self.setup_details()

    def setup_variables(self):
        list_pdbfiles = glob(os.path.join(self.path, '*.pdb'))
        if len(list_pdbfiles) == 0:
            self.pdb_file = None
        elif len(list_pdbfiles) == 1:
            self.pdb_file = os.path.basename(list_pdbfiles[0])
        else:
            self.pdb_file = [os.path.basename(f) for f in list_pdbfiles]
            raise NotImplementedError("Not implemented more then one pdb file")

    def event_press_show(self):
        """
        Event which is called to display the pymolwidget
        """
        print(self.layout_display.removeWidget(self.pushButtonShow))
        self.pushButtonShow.deleteLater()
        # show the display
        self.setup_display()

    def setup_display(self):
        """
        Function to display the structure
        """
        if self.pdb_file is not None:
            # setup pymolWidget
            self.pymolWidget = PyMolWidget(self)  # start pymolwidget
            self.pymolWidget.initializedGL.connect(
                lambda: self.pymolWidget.loadMolFile(os.path.join(self.path, self.pdb_file)))
            self.pymolWidget.setFixedWidth(400)  # set width
            self.pymolWidget.setFixedHeight(self.pymolWidget.width())  # make it squarewise
            self.layout_display.addWidget(self.pymolWidget)  #
            self.layout_displayside.addStretch(1)  # add a strech area below (so it will be at the top always)

            #
        else: # Todo: Implement several pdb files if found
            return


    def setup_details(self):
        """
        Setup the details
        """




        self.infoText = QLabel()
        if self.pdb_file is not None:
            u = MDAnalysis.Universe(os.path.join(self.path,self.pdb_file))
            ts = u.trajectory[0]

            # add the total number of atoms
            n_atoms= u.atoms.n_atoms
            text = "N(total)   : {}\n".format(n_atoms)

            # if we find a protein add it
            n_atoms_protein = u.select_atoms('protein').n_atoms
            if n_atoms_protein != 0:
                text += "N(protein) : {}\n".format(n_atoms_protein)

            # if we find n_atoms_solvent add the
            resname_water = ["SOL", "WATER", "SOLV", "mW", "H2O"]
            cond_water = " or ".join(["resname {}".format(i) for i in resname_water])
            n_atoms_solvent = u.select_atoms(cond_water).n_atoms
            if n_atoms_solvent != 0:
                text+= "N(solvent) : {}\n".format(n_atoms_solvent)

            # add box info
            text+= "\nBox (a,b,c, alpha, beta, gamma):\n{}".format(ts.dimensions)
        else:
            text="No pdb file found!"

        self.infoText.setText(text)
        self.infoText.setAlignment(Qt.AlignTop)
        self.layout_details.addWidget(self.infoText)
        self.infoText.setFont(QFont("Monospace"))

if __name__ == '__main__':
    import sys


    #sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    path = os.path.join(os.path.realpath(pkg_resources.resource_filename('old_labjournal', ''))
                        , "../tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD")
    window = MDSystemOverview(path = path)

    try:
        import qdarkstyle  # style

        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except:
        pass
    window.show()
    sys.exit(app.exec_())
