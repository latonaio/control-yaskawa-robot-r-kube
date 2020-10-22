#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 32

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "Axes01": self.AXES_01,
            "Axes02": self.AXES_02,
            "Axes03": self.AXES_03,
            "Axes04": self.AXES_04,
            "Axes05": self.AXES_05,
            "Axes06": self.AXES_06,
            "Axes07": self.AXES_07,
            "Axes08": self.AXES_08,
        }

    @property
    def AXES_01(self):
        return self._string_decoder(self.binary[0:4])

    @AXES_01.setter
    def AXES_01(self, v):
        self._set_bytes(0, v.decode(self.encode)[0:4])

    @property
    def AXES_02(self):
        return self._string_decoder(self.binary[4:8])

    @AXES_02.setter
    def AXES_02(self, v):
        self._set_bytes(4, v.decode(self.encode)[0:4])

    @property
    def AXES_03(self):
        return self._string_decoder(self.binary[8:12])

    @AXES_03.setter
    def AXES_03(self, v):
        self._set_bytes(8, v.decode(self.encode)[0:4])

    @property
    def AXES_04(self):
        return self._string_decoder(self.binary[12:16])

    @AXES_04.setter
    def AXES_04(self, v):
        self._set_bytes(12, v.decode(self.encode)[0:4])

    @property
    def AXES_05(self):
        return self._string_decoder(self.binary[16:20])

    @AXES_01.setter
    def AXES_01(self, v):
        self._set_bytes(16, v.decode(self.encode)[0:4])

    @property
    def AXES_06(self):
        return self._string_decoder(self.binary[20:24])

    @AXES_06.setter
    def AXES_06(self, v):
        self._set_bytes(20, v.decode(self.encode)[0:4])

    @property
    def AXES_07(self):
        return self._string_decoder(self.binary[24:28])

    @AXES_07.setter
    def AXES_07(self, v):
        self._set_bytes(24, v.decode(self.encode)[0:4])

    @property
    def AXES_08(self):
        return self._string_decoder(self.binary[28:32])

    @AXES_08.setter
    def AXES_08(self, v):
        self._set_bytes(32, v.decode(self.encode)[0:4])
