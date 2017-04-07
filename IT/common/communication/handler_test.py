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
from common.communication.communicationvalues import CommunicationValues


def main():
    comm = CommunicationValues()
    print("run")
    comm.send_hello()
    comm.send_course(1)

    comm.send_start()
    # time.sleep(2)
    # comm.send_letter(2)
    # time.sleep(1)
    # comm.send
    # print(comm.get_hello_blocking())
    # comm.send_start()
    # print(comm.get_start())
    count = 0
    # while count <= 1000:
    #    comm.send_error(count)
    #    count += 1
    # time.sleep(1)
    # while count >= 0:
    #    print(comm.get_error())
    #    count -= 1

    time.sleep(9000)






# ================================================================================
# main routine
# ================================================================================
if __name__ == '__main__':
    main()
