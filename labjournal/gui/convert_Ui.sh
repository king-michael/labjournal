#!/bin/bash

# convert Ui_MainWindow
pyuic5 Ui_MainWindow.ui -o Ui_MainWindow.py

pushd popups

# convert Ui_DialogNewEntry
pyuic5 Ui_DialogNewEntry.ui -o Ui_DialogNewEntry.py

popd # popups

pushd tabs
    # convert Ui_LabJournalTree
    pyuic5 Ui_LabJournalTree.ui -o Ui_LabJournalTree.py

    pushd InfoEntry
        # convert Ui_InfoEntry
        pyuic5 Ui_InfoEntry.ui -o Ui_InfoEntry.py

    popd # InfoEntry

popd # tabs