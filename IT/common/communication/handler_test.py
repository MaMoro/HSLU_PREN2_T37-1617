# ================================================================================
# !/usr/bin/python
# TITLE           : main.py
# DESCRIPTION     : Tests
# AUTHOR          : Moro Marco I.BSCI_F14.1301 <marco.moro@stud.hslu.ch>
# DATE            : 30.01.2017
# USAGE           :
# VERSION         : 0.1
# USAGE           :
# NOTES           :
# PYTHON_VERSION  : 3.4.2
# OPENCV_VERSION  : 3.1.0
# ================================================================================
import time
from common.communication.communicationhandler import SerialCommunicationHandler

from common.communication.communicationvalues import CommunicationValues


def main_old():
    comm = SerialCommunicationHandler().start()
    time.sleep(2)
    comm.send("method",1)
    comm.send("method",2)
    comm.send("method",3)
    comm.send("method",4)
    comm.send("method",5)
    comm.send("method",6)
    comm.send("method",7)
    comm.send("method",8)
    comm.send("method",9)
    comm.send("method",10)
    comm.send("method",11)
    comm.send("method",254)
    comm.send("method",255)
    time.sleep(0.5)
    print(comm.receive())
    comm.send("uii",33)
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    print(comm.receive())
    #print(comm.receive())


def main():
    comm = CommunicationValues().start()
    comm.send_hello()
    print(comm.get_hello())
    time.sleep(1)
    print(comm.get_hello())





# ================================================================================
# main routine
# ================================================================================
if __name__ == '__main__':
    main()
