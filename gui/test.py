from __future__ import print_function
import sys
from PyQt4 import QtCore

# END Import System Packages

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

# BEGIN Import GuiApplications
from Ui_MainWindow import *
from gui.tabs.InfoEntry.LAMMPS.WidgetThermo import WidgetThermo
# END Import GuiApplications
# my modules
sys.path.append('..')
from core import *
from core.logger import Logger

__author__              = ["Michael King"]
__date__                = "29.09.2017"


# Text Handling
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# BEGIN TESTS
log = Logger()

dic_modes = {
    'LAMMPS' : "LAMMPS"
}

class main():
    def __init__(self, state=True):
        '''MainClass'''
        if state:
            self.start_app()
            self.start_window()
            self.show_gui()

    def start_app(self):
        self.app = QtGui.QApplication(sys.argv)
        return self.app

    def start_window(self):
        self.window = MainWindow()
        # setup stylesheet
        try:
            import qdarkstyle  # style
            self.app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
        except:
            pass
        return self.window

    def show_gui(self):
        self.window.show()

    def restart_gui(self):
        self.start_window()
        self.show_gui()

    def __del__(self):
        '''Destruction of class'''
        sys.exit(app.exec_())
# END TESTS

#=============================================================================#
# class GuiMainWindow
#=============================================================================#

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__()

        self.path = os.path.join("/home/micha/SIM-PhD-King/labjournal/tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/production")

        layout_body=self.layout()
        if layout_body is None:
            layout_body = QtGui.QVBoxLayout(self)
        btn = QtGui.QPushButton("Open Thermo Data")
        btn.clicked.connect(self.PopUp_WidgetThermo)
        layout_body.addWidget(btn)


    def PopUp_WidgetThermo(self):
        widgetthermo = WidgetThermo(path=self.path)
        widgetthermo.show()

#=============================================================================#
# Tests
#=============================================================================#

if __name__ == '__main__':
    if not 'GUI' in locals():
        GUI = main(False)  # fix to use in notebook
        app = GUI.start_app()
        window = GUI.start_window()
        GUI.show_gui()
    else:
        GUI.restart_gui()
    # FIXME: we need sys.exit(app.exec_()) or the plot from matplotlib will not be displayed
    sys.exit(app.exec_())