# ================================================================================
# !/usr/bin/python
# TITLE           : fpshelper.py
# DESCRIPTION     : FPS Calculator Helper
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 17/11/2016
# USAGE           :
# VERSION         : 0.1
# ================================================================================

# import the necessary packages
from timeit import default_timer as timer


class FPSHelper(object):
    """
    Simple Logging Helper. Returns logger reference.
    """

    def __init__(_self):
        # store the start time, end time that were examined between the start and end intervals
        _self._start = None
        _self._end = None

    def start(_self):
        # start the timer
        _self._start = timer()
        return _self

    def stop(_self):
        # stop the timer
        _self._end = timer()

    def elapsedtime_ms(_self):
        # return the total number of milliseconds between the start and end interval
        return (_self._end - _self._start) * 1000.0

    def elapsedtime_sec(_self):
        # return the total number of seconds between the start and end interval
        return (_self._end - _self._start)

    def fps(_self):
        # compute the (approximate) frames per second
        return 1 / _self.elapsedtime_sec()
