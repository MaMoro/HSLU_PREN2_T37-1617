# ================================================================================
# !/usr/bin/python
# TITLE           : communicationvalues.py
# DESCRIPTION     : Operational commands and values for serial communication
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
import time

import common.config.confighandler as cfg
from threading import Thread
from logging.config import fileConfig
from common.communication.serialcommunicationhandler import SerialCommunicationHandler


class CommunicationValues(object):
    class __CommunicationValues:
        def __init__(self):
            fileConfig(cfg.get_logging_config_fullpath())
            self.__log = logging.getLogger()
            self.op_hello = None
            self.op_start = None
            self.op_course = None
            self.op_tof_l_i = 0
            self.op_tof_l_s = 0
            self.op_tof_r_i = 0
            self.op_tof_r_s = 0
            self.op_tof_f_i = 0
            self.op_tof_f_s = 0
            self.op_raupe_l_i = 0
            self.op_raupe_l_s = 0
            self.op_raupe_r_i = 0
            self.op_raupe_r_s = 0
            self.op_gyro_n = 0
            self.op_gyro_g = 0
            self.op_gyroskop_i = 0
            self.op_gyroskop_s = 0
            self.op_servo_s = 0
            self.op_servo_i = 0
            self.op_letter = None
            self.op_parcstate = None
            self.op_errstate = None
            self.timeout = 0.3
            self.__serialcomm = SerialCommunicationHandler().start()
            time.sleep(1)

        def get_hello_blocking(self):
            hellocounter = 0
            while self.op_hello is None:
                if hellocounter < 20:
                    time.sleep(self.timeout)
                    hellocounter += 1
                else:
                    self.__log.error("timeout hello blocking...")
                    break
            return self.op_hello

        def get_hello(self):
            return self.op_hello

        def get_start(self):
            return self.op_start

        def get_course(self):
            return self.op_course

        def get_tof_left(self):
            return self.op_tof_l_i

        def get_tof_right(self):
            return self.op_tof_r_i

        def get_tof_front(self):
            return self.op_tof_f_i

        def get_raupe_left(self):
            return self.op_raupe_l_i

        def get_raupe_right(self):
            return self.op_raupe_r_i

        def get_gyroskop(self):
            return self.op_gyroskop_i

        def get_servo(self):
            return self.op_servo_i

        def get_parcstate(self):
            return self.op_parcstate

        def get_error(self):
            return self.op_errstate

        def send_hello(self):
            self.__serialcomm.send("hello", 1)
            hellocounter = 0
            while self.op_hello is None:
                time.sleep(0.05)
                if hellocounter < 20:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("hello", 1)
                    hellocounter += 1
                else:
                    self.__log.error("hello message not acknowledged")

        def send_start(self):
            self.__serialcomm.send("start", 1)
            startcounter = 0
            while self.op_start is None:
                if startcounter < 20:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("start", 1)
                    startcounter += 1
                else:
                    self.__log.error("start signal not acknowledged")

        def send_course(self, course):
            self.__serialcomm.send("course", course)
            coursecounter = 0
            while self.op_course is None:
                if coursecounter < 20:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("course", course)
                    coursecounter += 1
                else:
                    self.__log.error("course selection not acknowledged")

        def send_letter(self, detectedletter):
            self.__serialcomm.send("letter", detectedletter)
            lettercounter = 0
            while self.op_letter is None:
                if lettercounter < 20:
                    time.sleep(self.timeout)
                    self.__serialcomm.send("letter", detectedletter)
                    lettercounter += 1
                else:
                    self.__log.error("letter not acknowledged")

        def send_tof_left(self, value):
            if self.op_tof_l_s != value:
                self.__serialcomm.send("tof_l_s", value)

        def send_tof_right(self, value):
            if self.op_tof_r_s != value:
                self.__serialcomm.send("tof_r_s", value)

        def send_tof_front(self, value):
            if self.op_tof_f_s != value:
                self.__serialcomm.send("tof_f_s", value)

        def send_raupe_left(self, value):
            if self.op_raupe_l_s != value:
                self.__serialcomm.send("raupe_l_s", value)

        def send_raupe_right(self, value):
            if self.op_raupe_r_s != value:
                self.__serialcomm.send("raupe_r_s", value)

        def send_gyroskop(self, value):
            if self.op_gyroskop_s_s != value:
                self.__serialcomm.send("gyroskop_s", value)

        def send_servo(self, value):
            if self.op_servo_s != value:
                self.__serialcomm.send("servo_s", value)

        def send_error(self, value):
            if self.op_errstate != value:
                self.__serialcomm.send("errstate", value)

        def __handleoperations(self):
            while True:
                operation, value = self.__serialcomm.receive()
                # self.__log.info("got op:" + str(operation) + " val: " + str(value))
                if operation == "hello":
                    if value == '1':
                        self.op_hello = 1
                elif operation == "start":
                    if value == '1':
                        self.op_start = 1
                elif operation == "course":
                    self.op_course = '1'
                elif operation == "tof_l_i":
                    self.op_tof_l_i = value
                elif operation == "tof_r_i":
                    self.op_tof_r_i = value
                elif operation == "tof_f_i":
                    self.op_tof_f_i = value
                elif operation == "raupe_l_i":
                    self.op_raupe_l_i = value
                elif operation == "raupe_r_i":
                    self.op_raupe_r_i = value
                elif operation == "gyro_n":
                    self.op_gyro_n = value
                elif operation == "gyro_g":
                    self.op_gyro_g = value
                elif operation == "gyroskop_i":
                    self.op_gyroskop_i = value
                elif operation == "servo_i":
                    self.op_servo_i = value
                elif operation == "letter":
                    self.op_letter = value
                elif operation == "parcstate":
                    self.op_parcstate = value
                elif operation == "errstate":
                    self.op_errstate = value
                    self.__log.error("got error from FRDM: " + value)
                else:
                    self.__log.warning("got unknown operation: " + str(operation) + " with val: " + str(value))

        def start(self):
            thread = Thread(target=self.__handleoperations, args=())
            thread.daemon = True
            thread.start()
            return self

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CommunicationValues.instance:
            CommunicationValues.instance = CommunicationValues.__CommunicationValues()
        return CommunicationValues.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
