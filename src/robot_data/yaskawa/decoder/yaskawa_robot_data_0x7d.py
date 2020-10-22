#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import struct

from .yaskawa_robot_data import YaskawaRobotData 

class RobotData(YaskawaRobotData):
    data_size = 4

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "Float": self.FLOAT_VALUE,
            }

    @property
    def FLOAT_VALUE(self):
        return struct.unpack("<f" if self.byte_order == "little" else "f", bytes(self.binary[0:4]))
    @FLOAT_VALUE.setter
    def FLOAT_VALUE(self, v):
        struct.pack("<f" if self.byte_order == "little" else "f", v)
