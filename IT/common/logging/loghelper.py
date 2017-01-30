# ================================================================================
# !/usr/bin/python
# TITLE           : loghelper.py
# DESCRIPTION     : Helper Log Class
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 24.11.2016
# USAGE           : log=LogHelper() and log.warn("upss")
# VERSION         : 0.2
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
        _self._minLogLevel = int(config['settings']['loglevel'])
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.DEBUG)

    def debug(_self, message):
        if _self._minLogLevel == logging.DEBUG:
            _self._log.debug(message)

    def info(_self, message):
        if _self._minLogLevel <= logging.INFO:
            _self._log.info(message)

    def warn(_self, message):
        if _self._minLogLevel <= logging.WARN:
            _self._log.warning(message)

    def error(_self, message):
        # always show errors regardless of preferred loglevel
        _self._log.error(message)
