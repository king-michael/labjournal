#!/bin/bash

echo "Copy test.db to all subfolders where its needed (for testing only)"

INPUT=tests/test_dbs/test.db
OUTPUT=()
OUTPUT+=(core/)
OUTPUT+=(gui/)
OUTPUT+=(gui/tabs/)
OUTPUT+=(gui/tabs/InfoEntry/)
OUTPUT+=(gui/tabs/InfoEntry/LAMMPS/)

for path in ${OUTPUT[@]}; do
  echo "cp $INPUT $path/tmp.db"
  cp $INPUT $path/tmp.db
done
