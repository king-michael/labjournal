#!/bin/bash

export PATH=$PWD:$PATH # so we can use the pyuic5 laying here

# convert Ui_MainWindow
for file_ui in $(ls Ui_*.ui); do
  fname=${file_ui%%.ui}
  echo ${fname}
  pyuic5 ${fname}.ui -o ${fname}.py
done

