#!/bin/bash

# convert Ui_MainWindow
pyuic4 MainWindow.ui -o MainWindow.py


pushd tabs
    # convert Ui_LabJournalTree
    pyuic4 Ui_LabJournalTree.ui -o LabJournalTree.py

    pushd InfoEntry
        # convert Ui_InfoEntry
        pyuic4 Ui_InfoEntry.ui -o InfoEntry.py

    popd # InfoEntry

popd # tabs