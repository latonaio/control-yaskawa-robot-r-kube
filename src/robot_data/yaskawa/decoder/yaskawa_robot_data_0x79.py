#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 2

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "Register": self.REGISTER,
        }

    @property
    def REGISTER(self):
        return int.from_bytes(self.binary[0:2], byteorder=self.byte_order)

    @REGISTER.setter
    def REGISTER(self, v):
        self._set_bytes(0, v.to_bytes(4, self.byte_order)[0:2])
