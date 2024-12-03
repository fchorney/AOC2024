#!/bin/sh


mkdir -vp $1
cp -v template.py $1/solution.py
touch $1/test_input_1.txt

exit 0
