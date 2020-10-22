#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData 

class RobotData(YaskawaRobotData):
    data_size = 1

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "IO": self.IO,
            }

    @property
    def IO(self):
        return int.from_bytes(self.binary[0:1], byteorder=self.byte_order)
    @IO.setter
    def IO(self, v):
        self._set_bytes(0, v.to_bytes(4, self.byte_order)[0:1])
