#!/bin/bash

# convert UiMain
pyuic4 UiMainWindow.ui -o UiMainWindow.py

# convert Ui_tab_LabJournalTree
pyuic4 Ui_tab_LabJournalTree.ui -o Ui_tab_LabJournalTree.py

# convert Ui_tab_InfoEntry_LAMMPS
pyuic4 Ui_tab_InfoEntry_LAMMPS.ui -o Ui_tab_InfoEntry_LAMMPS.py