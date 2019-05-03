#!/bin/bash

#Check for Pyhton, install if not insalled
apt-get install python python-tk -y
echo 'Python and python-tk is installed.'
python configurator.py