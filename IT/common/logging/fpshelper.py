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

    def __init__(self):
        # store the start time, end time that were examined between the start and end intervals
        self._start = None
        self._end = None

    def start(self):
        # start the timer
        self._start = timer()
        return self

    def stop(self):
        # stop the timer
        self._end = timer()

    def elapsedtime_ms(self):
        # return the total number of milliseconds between the start and end interval
        return (self._end - self._start) * 1000.0

    def elapsedtime_sec(self):
        # return the total number of seconds between the start and end interval
        return (self._end - self._start)

    def fps(self):
        # compute the (approximate) frames per second
        return int(1 / self.elapsedtime_sec())
