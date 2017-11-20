#!/bin/bash
# script to build testcase folders

FOLDER_TEMPLATES=templates

CREATEDFOLDERS=()
for folder in `ls $FOLDER_TEMPLATES`; do
    FOLDER_TESTCASE=testcase_$folder
    echo "Remove $FOLDER_TESTCASE"
    rm -rf $FOLDER_TESTCASE
    echo "Create $FOLDER_TESTCASE"
    cp -a $FOLDER_TEMPLATES/$folder ./$FOLDER_TESTCASE
    CREATEDFOLDERS+=("$FOLDER_TESTCASE")
done

echo "Created folders:"
for i in ${CREATEFOLDERS[@]}; do echo " $i"; done
echo "Finished creating testcase_* folders"