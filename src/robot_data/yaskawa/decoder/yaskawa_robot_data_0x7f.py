#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 52

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "ParameterSet": self.PARAMETER_SET,
            "RobotForm": self.ROBOT_FORM,
            "ToolNo": self.TOOL_NO,
            "UserCoordinates": self.USER_COORDINATE,
            "RobotFormExtension": self.ROBOT_FORM_EXTENSION,
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
    def PARAMETER_SET(self):
        return int.from_bytes(self.binary[0:4], byteorder=self.byte_order)

    @PARAMETER_SET.setter
    def PARAMETER_SET(self, v):
        self._set_bytes(0, v.to_bytes(4, self.byte_order))

    @property
    def ROBOT_FORM(self):
        return self._byte_to_bits(int.from_bytes(self.binary[4:8], byteorder=self.byte_order))

    @ROBOT_FORM.setter
    def ROBOT_FORM(self, v):
        self._set_bytes(4, [self._bits_to_byte(v), 0, 0, 0])

    @property
    def TOOL_NO(self):
        return int.from_bytes(self.binary[8:12], byteorder=self.byte_order)

    @TOOL_NO.setter
    def TOOL_NO(self, v):
        self._set_bytes(8, v.to_bytes(4, self.byte_order))

    @property
    def USER_COORDINATE(self):
        return int.from_bytes(self.binary[12:16], byteorder=self.byte_order)

    @USER_COORDINATE.setter
    def USER_COORDINATE(self, v):
        self._set_bytes(12, v.to_bytes(4, self.byte_order))

    @property
    def ROBOT_FORM_EXTENSION(self):
        return self._byte_to_bits(int.from_bytes(self.binary[16:20], byteorder=self.byte_order))

    @ROBOT_FORM_EXTENSION.setter
    def ROBOT_FORM_EXTENSION(self, v):
        self._set_bytes(16, [self._bits_to_byte(v), 0, 0, 0])

    @property
    def AXES_01(self):
        return int.from_bytes(self.binary[20:24], byteorder=self.byte_order, signed=True) / 1000

    @AXES_01.setter
    def AXES_01(self, v):
        self._set_bytes(20, v.to_bytes(4, self.byte_order))

    @property
    def AXES_02(self):
        return int.from_bytes(self.binary[24:28], byteorder=self.byte_order, signed=True) / 1000

    @AXES_02.setter
    def AXES_02(self, v):
        self._set_bytes(24, v.to_bytes(4, self.byte_order))

    @property
    def AXES_03(self):
        return int.from_bytes(self.binary[28:32], byteorder=self.byte_order, signed=True) / 1000

    @AXES_03.setter
    def AXES_03(self, v):
        self._set_bytes(28, v.to_bytes(4, self.byte_order))

    @property
    def AXES_04(self):
        return int.from_bytes(self.binary[32:36], byteorder=self.byte_order, signed=True) / 10000

    @AXES_04.setter
    def AXES_04(self, v):
        self._set_bytes(32, v.to_bytes(4, self.byte_order))

    @property
    def AXES_05(self):
        return int.from_bytes(self.binary[36:40], byteorder=self.byte_order, signed=True) / 10000

    @AXES_05.setter
    def AXES_05(self, v):
        self._set_bytes(36, v.to_bytes(4, self.byte_order))

    @property
    def AXES_06(self):
        return int.from_bytes(self.binary[40:44], byteorder=self.byte_order, signed=True) / 10000

    @AXES_06.setter
    def AXES_06(self, v):
        self._set_bytes(40, v.to_bytes(4, self.byte_order))

    @property
    def AXES_07(self):
        return int.from_bytes(self.binary[44:48], byteorder=self.byte_order)

    @AXES_07.setter
    def AXES_07(self, v):
        self._set_bytes(44, v.to_bytes(4, self.byte_order))

    @property
    def AXES_08(self):
        return int.from_bytes(self.binary[48:52], byteorder=self.byte_order)

    @AXES_08.setter
    def AXES_08(self, v):
        self._set_bytes(48, v.to_bytes(4, self.byte_order))
