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

import sys,os
from functools import partial
from copy import deepcopy
root = '../../../../'  # path to root dir
sys.path.insert(0,root)  # append root dir
from core.settings import settings

from PyQt4 import QtGui, QtCore

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import random

from analysis.LAMMPS.thermo import Thermo

class WidgetThermo(QtGui.QWidget):
    def __init__(self, **kwargs):
        """A Widget to plot Thermo Data"""
        self.kwargs = kwargs
        super(WidgetThermo, self).__init__()
        self.setupUi()

        self.CWD = self.kwargs['path'] if "path" in self.kwargs.keys() else os.path.realpath(os.path.curdir)
        # Default settings:

        self.initialisation()

    def initialisation(self):
        """Initialisation protocol"""
        # create the thermo object / data
        self.thermo = Thermo(path=self.CWD)

        self.list_keywords=deepcopy(self.thermo.possible_keywords)

        try:
            self.list_active_keywords =settings['LAMMPS']['thermo']['list_keywords']
        except:
            self.list_active_keywords = []  # list of active keywords

        # ToDo: Add exception handling if keyword is not here
        # ToDo: add handling for time OR Step
        try:
            self.xlabel = self.settings['LAMMPS']['thermo']['xlabel']
        except:
            self.xlabel = "Step"  # self.settings['LAMMPS']['thermo']['xlabel']

        for key in ['Step','Time']:
            if key in self.list_keywords:
                self.list_keywords.remove(key)

        # Add the checkboxes
        for keyword in self.list_keywords:
            checkbox=QtGui.QCheckBox()
            checkbox.setText(keyword)
            if keyword in self.list_active_keywords:
                checkbox.setCheckState(QtCore.Qt.Checked)
            checkbox.stateChanged.connect(partial(self.checkbox_stateChanged, checkbox))
            self.layout_checkboxes.addWidget(checkbox)
        self.refresh_plot()

    def checkbox_stateChanged(self,checkbox):
        """Function call when checkbox state is changed"""
        keyword=str(checkbox.text())
        print(self.list_active_keywords)
        if checkbox.isChecked():
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
            print(keyword)
            self.plot_thermo(keyword)

    def plot_thermo(self,keyword):
        """plot thermo data"""
        self.plot(self.thermo[self.xlabel],self.thermo[keyword])


    def setupUi(self):
        """Create the Ui"""
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # This is the layout for checkboxes (to be filled later)
        self.layout_checkboxes=QtGui.QHBoxLayout()

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addLayout(self.layout_checkboxes)
        self.setLayout(layout)

    def init_plot(self):
        # create an axis
        self.ax = self.figure.add_subplot(111)
        # discards the old graph
        self.ax.clear()

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