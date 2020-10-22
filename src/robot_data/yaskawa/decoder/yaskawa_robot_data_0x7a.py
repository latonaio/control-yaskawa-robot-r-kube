#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData 

class RobotData(YaskawaRobotData):
    DATA_SIZE = 1

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "Byte": self.byte_value,
            }

    @property
    def byte_value(self):
        return self.binary[0:1]

    @byte_value.setter
    def byte_value(self, v):
        self._set_bytes(0, v)
