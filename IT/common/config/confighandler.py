# ================================================================================
# !/usr/bin/python
# TITLE           : confighandler.py
# DESCRIPTION     : Handler for config file
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================

# import the necessary packages
import logging
import configparser

config = configparser.ConfigParser()
config.read('/home/pi/Desktop/PREN/common/config.ini')


def str2bool(v):
    return v.lower() in ("yes", "Yes", "YES", "true", "True", "TRUE", "1", "t")


class LogHelper:
    """
    Simple Logging Helper. Returns logger reference.
    """

    def __init__(_self):
        _self._log = logging.getLogger()
        print("TODO")

    def read(_self, message):
        print("TODO")

    def write(_self, message):
        print("TODO")
