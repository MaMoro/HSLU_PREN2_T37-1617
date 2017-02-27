# ================================================================================
# !/usr/bin/python
# TITLE           : parcoursstate.py
# DESCRIPTION     : Parcour states as enum
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
from enum import Enum


class ParcoursState(Enum):
     NotInitalized = 0
     Setup = 1
     StartField = 2
     Treppe = 3
     Verschrenkung = 4
     Wendebereich = 5
     Torbogen = 6
     Bodenwelle = 7
     Wippe = 8
     Lichtschranke = 9
     Taster = 10
     Error = 99