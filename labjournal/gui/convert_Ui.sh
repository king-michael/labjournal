#!/bin/bash

export PATH=$PWD:$PATH # so we can use the pyuic5 laying here

# convert Ui_MainWindow
pyuic5 Ui_MainWindow.ui -o Ui_MainWindow.py

pushd popups

    # convert Ui_DialogNewEntry
    pyuic5 Ui_DialogNewEntry.ui -o Ui_DialogNewEntry.py

    pushd DialogSettings
         pyuic5 Ui_DialogSettings.ui -o Ui_DialogSettings.py
    popd # DialogSettings


popd # popups

pushd tabs
    # convert Ui_LabJournalTree
    pyuic5 Ui_LabJournalTree.ui -o Ui_LabJournalTree.py

    pushd InfoEntry
        # convert Ui_InfoEntry
        pyuic5 Ui_InfoEntry.ui -o Ui_InfoEntry.py

        # convert SystemOverview
        pushd general/MDSystemOverview
            pyuic5 Ui_MDSystemOverview.ui  -o Ui_MDSystemOverview.py
        popd # general/MDSystemOverview
    popd # InfoEntry

popd # tabs