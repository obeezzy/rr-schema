#/bin/bash

if [ $# -ge 2 ]
then
    PYTHONPATH=. python3 -m unittest discover -s $1 -p $2 -v
elif [ $# -ge 1 ]
then
    PYTHONPATH=. python3 -m unittest discover -s $1 -v
else
    PYTHONPATH=. python3 -m unittest discover -s proctests -v
fi