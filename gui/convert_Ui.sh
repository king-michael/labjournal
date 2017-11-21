#!/bin/bash

# convert Ui_MainWindow
pyuic4 Ui_MainWindow.ui -o GUi_MainWindow.py


pushd tabs
    # convert Ui_LabJournalTree
    pyuic4 Ui_LabJournalTree.ui -o GUi_LabJournalTree.py

    pushd InfoEntry
        # convert Ui_InfoEntry
        pyuic4 Ui_InfoEntry.ui -o GUi_InfoEntry.py

    popd # InfoEntry

popd # tabs