#!/bin/bash
INFO="""
Creates a file with all ToDo statements
Creates a file with all FixMe statements
"""

#=========================================================#
# ToDo statements
#=========================================================#
OUTFILE=todo.txt

echo "# $(date)" > $OUTFILE

for file in `find . -type f`; do
  if grep -iFq "ToDo" $file ; then
    case $file in
       "./$0")
       ;;
       "./$OUTFILE")
       ;;
       ./.idea*)
       ;;
       *)     
        grep -i 'ToDo' $file | while read -r line ; do
          echo "$file : $line"  >> $OUTFILE
        done
      ;;
    esac
  fi
done

cat $OUTFILE

#=========================================================#
# FIXME statements
#=========================================================#
OUTFILE=fixme.txt

echo "# $(date)" > $OUTFILE

for file in `find . -type f`; do
  if grep -iFq "FIXME" $file ; then
    case $file in
       "./$0")
       ;;
       "./$OUTFILE")
       ;;
       ./.idea*)
       ;;
       *)
        grep -i 'FIXME' $file | while read -r line ; do
          echo "$file : $line"  >> $OUTFILE
        done
      ;;
    esac
  fi
done

cat $OUTFILE
