#!/usr/bin/env python
"""
# Details:
#   PopUp Window for ThermoData
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

import os
import sys
from copy import deepcopy

root = '../../../../'  # path to root dir
sys.path.insert(0,root)  # append root dir

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSettings
settings = QSettings('foo', 'foo')

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from labjournal.analysis.LAMMPS.thermo import Thermo

class WidgetThermo(QtGui.QWidget):
    def __init__(self, **kwargs):
        """A Widget to plot Thermo Data"""
        self.kwargs = kwargs
        super(WidgetThermo, self).__init__()
        self.SIZE=[400,400]
        self.OPTION_TOOLBAR=True
        self.OPTION_LEGEND=True
        for k,v in kwargs.iteritems(): # apply kwargs
             setattr(self,k,v)
        self.resize(*self.SIZE)
        self.setupUi()

        self.CWD = self.kwargs['path'] if "path" in self.kwargs.keys() else os.path.realpath(os.path.curdir)

        self.initialisation()

    def initialisation(self):
        """Initialisation protocol"""
        # create the thermo object / data
        if hasattr(self,'logfile'):
            self.thermo = Thermo(logfile=self.logfile)
        else:
            self.thermo = Thermo(path=self.CWD)

        self.list_keywords=deepcopy(self.thermo.possible_keywords)


        self.list_active_keywords= [str(i.toString()) for i in settings.value('LAMMPS/thermo/list_keywords',
                                    ['PotEng', 'Temp', 'Press', 'Volume']).toList()]

        # ToDo: Add exception handling if keyword is not here
        # ToDo: add handling for time OR Step

        self.xlabel = str(settings.value('LAMMPS/thermo/xlabel', 'Step').toString())

        for key in ['Step','Time']:
            if key in self.list_keywords:
                self.list_keywords.remove(key)

        self.toolbutton = QtGui.QToolButton(self)
        self.toolbutton.setText('Select Keywords ')
        self.toolmenu = QtGui.QMenu(self)
        for keyword in self.list_keywords:
            action = self.toolmenu.addAction(keyword)
            action.setCheckable(True)
            action.triggered[()].connect(lambda item=action: self.toolmenu_triggered(item))
            if keyword in self.list_active_keywords:
                action.setChecked(QtCore.Qt.Checked)
        self.toolbutton.setMenu(self.toolmenu)
        self.toolbutton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.layout_checkboxes.addWidget(self.toolbutton)

        DPI = self.figure.get_dpi()
        self.figure.set_size_inches((self.SIZE[0]-self.toolbutton.sizeHint().height()) / float(DPI),
                                     self.SIZE[1] / float(DPI))
        self.refresh_plot()

    def toolmenu_triggered(self,item):
        """Function call when checkbox state is changed"""
        keyword=str(item.text())
        if item.isChecked():
            if not keyword in self.list_active_keywords:
                self.list_active_keywords.append(keyword)
        else:
            if keyword in self.list_active_keywords:
                self.list_active_keywords.remove(keyword)
        self.refresh_plot()

    def refresh_plot(self):
        """Refresh the plot and plot active keywords"""
        if hasattr(self, 'ax'):
            self.ax.clear()
        for keyword in self.list_active_keywords:
            self.plot_thermo(keyword)

        if self.OPTION_LEGEND:
            lines, labels = self.ax.get_legend_handles_labels()
            self.ax.legend(lines, labels, loc=0)
            self.canvas.draw()
        self.figure.tight_layout()

    def plot_thermo(self,keyword):
        """plot thermo data"""
        self.plot(self.thermo[self.xlabel],self.thermo[keyword],label=keyword)


    def setupUi(self):
        """Create the Ui"""
        # a figure instance to plot on

        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        if self.OPTION_TOOLBAR:
            self.toolbar = NavigationToolbar(self.canvas, self)

        # This is the layout for checkboxes (to be filled later)
        self.layout_checkboxes=QtGui.QGridLayout()

        # set the layout
        layout = QtGui.QVBoxLayout()
        if self.OPTION_TOOLBAR:
            layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.layout_checkboxes)
        self.setLayout(layout)

    def init_plot(self):
        # create an axis
        self.ax = self.figure.add_subplot(111)
        # discards the old graph
        self.ax.clear()

    def set_size(self,size):
        """function to change the size"""
        #self.
        self.figure.set_size_inches(*size)

    def plot(self,*args,**kwargs):
        ''' plot some random stuff '''
        if not hasattr(self,'ax'):
            self.init_plot()

        self.ax.plot(*args,**kwargs)
        # draw
        self.canvas.draw()
        self.canvas.show()

if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)
    try:
        import qdarkstyle  # style
        app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    except:
        pass

    path = "tests/test_folder_structures/dummy_micha/dummy_folders/testcase_normalMD/production/"
    path=os.path.join(root,path)
    print("Use Path: {}".format(path))
    print("Files:")
    print(os.listdir(path))
    main = WidgetThermo(path=path)
    main.show()

    sys.exit(app.exec_())