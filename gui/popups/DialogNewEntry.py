"""
Dialog Window to create a new Database Entry

Todo:
  - add entries to QStringList dynamically
"""

import sys
import re
from PyQt4 import QtCore, QtGui
import logging
logger = logging.getLogger('LabJournal')

sys.path.append("../..")
from core.databaseModel import *

from Ui_DialogNewEntry import Ui_Dialog

class DialogNewEntry(QtGui.QDialog,Ui_Dialog):
    def __init__(self, parent = None):
        super(DialogNewEntry, self).__init__(parent)
        self.setupUi(self)

        # add a word completer to lineEdit_simtype
        sim_type_list=QtCore.QStringList(['LAMMPS', 'PYTHON'])
        sim_type_completer = QtGui.QCompleter(sim_type_list)
        sim_type_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.lineEdit_simtype.setCompleter(sim_type_completer)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.show()

    def getContent(self):
        """
        Function to return the content in form of a dictionary
        :return: adict
        """
        tags=[]
        keywords={}
        for i in re.split('\n|;', self.textEdit_tags.toPlainText()):
            STR=str(i)
            if len(STR) == 0: continue
            if STR.find('=') == -1:
                tags.append(STR)
            else:
                split = STR.split('=', 1)
                keywords[split[0]]=split[1]
        adict = dict(
            sim_id = self.lineEdit_simid.text(),
            mediawiki = self.lineEdit_mediawiki.text(),
            path = self.lineEdit_path.text(),
            sim_type = self.lineEdit_simtype.text(),
            description = self.textEdit_description.toPlainText(),
            tags = tags,
            keywords = keywords
        )
        if len(adict['sim_id']) == 0:
            print "ERROR"
        else:
            return adict

    def getDatabaseObjects(self):
        """Function to return the content in form of Database objects
        :return: Simulation, [keywords,]
        """
        assert self.lineEdit_simid.text() != 0, "SIMID have to be defined"


        keywords = []
        for i in re.split('\n|;', self.textEdit_tags.toPlainText()):
            STR=str(i)
            if len(STR) == 0: continue
            if STR.find('=') == -1:
                keywords.append(Keywords(
                    name=STR
                ))
            else:
                split = STR.split('=', 1)
                keywords.append(Keywords(
                    name=split[0],
                    value=split[1]
                ))
        sim = Simulation(
            sim_id=str(self.lineEdit_simid.text()),
            mediawiki=str(self.lineEdit_mediawiki.text()),
            path=str(self.lineEdit_path.text()),
            sim_type=str(self.lineEdit_simtype.text()),
            description=str(self.textEdit_description.toPlainText()),
            keywords=keywords
        )
        return sim

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getEntry(parent = None):
        dialog = DialogNewEntry(parent)
        result = dialog.exec_()
        sim = dialog.getDatabaseObjects()
        return (sim, result == QtGui.QDialog.Accepted)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    window = DialogNewEntry()

    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass
    window.show()
    sys.exit(app.exec_())