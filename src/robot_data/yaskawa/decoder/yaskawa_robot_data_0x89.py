#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 48

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "SystemVersion": self.SYSTEM_VERSION,
            "ControllerName": self.CONTROLLER_NAME,
            "ParameterVersion": self.PARAMETER_VERSION,
        }

    @property
    def SYSTEM_VERSION(self):
        return self._string_decoder(self.binary[0:24])

    @SYSTEM_VERSION.setter
    def SYSTEM_VERSION(self, v):
        self._set_bytes(0, v.decode(self.encode)[0:24])

    @property
    def CONTROLLER_NAME(self):
        return self._string_decoder(self.binary[24:40])

    @CONTROLLER_NAME.setter
    def CONTROLLER_NAME(self, v):
        self._set_bytes(24, v.decode(self.encode)[0:16])

    @property
    def PARAMETER_VERSION(self):
        return self._string_decoder(self.binary[40:48])

    @PARAMETER_VERSION.setter
    def PARAMETER_VERSION(self, v):
        self._set_bytes(40, v.decode(self.encode)[0:8])
