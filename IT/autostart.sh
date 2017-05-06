#!/bin/bash
# =======================================================================
# title           :autostart.sh
# description     :This program enables to start project at startup
# author          :Marco Moro
# date            :30.01.2016
# version         :0.1
# usage           :autostart.sh
# notes           :
# python_version  :3.4.2
# opencv_version  :3.1.0
# =======================================================================

sleep 3  # wait 5s to let RPi finish the start up procedure
/home/pi/.virtualenvs/cv/bin/python3 /home/pi/Desktop/PREN/main.py &
