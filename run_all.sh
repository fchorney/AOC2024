#!/bin/sh

for x in `find . -type d -regex "./[0-9][0-9]" | sort` ; do
    echo "Running Day $x"
    cd $x
    python solution.py run
    cd ..
    echo
done

exit 0
