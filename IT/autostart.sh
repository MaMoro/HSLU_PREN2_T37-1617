# =======================================================================
# title           :autostart.sh
# description     :This program enables to start project at startup
# author          :Marco Moro
# date            :30.01.2016
# version         :0.1
# usage           :sudo autostart.sh
# notes           :
# python_version  :3.4.2
# opencv_version  :3.1.0
# =======================================================================

#!/bin/bash
FILEPATH=/home/pi/Desktop
# !!!!!!!!!!!!!!! start this script with sudo !!!!!!!!!!!!!!!

sleep 3  # wait 3s to let RPi finish the start up procedure
python3 $FILEPATH/PREN/main.py > $FILEPATH/logging/run.log 2>&1 &
