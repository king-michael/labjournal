#

__author__ = ["Michael King"]
__date__ = "29.09.2017"

import logging
import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

from old_labjournal.gui.MainWindow import MainWindow

logger = logging.getLogger('LabJournal')

APPLICATION_NAME = 'foo'
COMPANY_NAME = 'foo'
settings = QSettings(APPLICATION_NAME, COMPANY_NAME)

app = None


class Main:
    def __init__(self, state=True):
        """MainClass"""
        if state:
            self.start_app()
            self.start_window()
            self.show_gui()

    def start_app(self):
        global app
        app = QApplication(sys.argv)
        return app

    def start_window(self):
        global app
        self.window = MainWindow()
        # setup stylesheet
        try:
            import qdarkstyle  # style
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
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


# =============================================================================#
# Tests
# =============================================================================#

if __name__ == '__main__':
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__),'../..')))  # add module to path
    logging.basicConfig(level=logging.DEBUG)
    if not 'GUI' in locals():
        GUI = Main(False)  # fix to use in notebook
        app = GUI.start_app()
        window = GUI.start_window()
        GUI.show_gui()
    else:
        GUI.restart_gui()
    # FIXME: we need sys.exit(app.exec_()) or the plot from matplotlib will not be displayed
    sys.exit(app.exec_())
