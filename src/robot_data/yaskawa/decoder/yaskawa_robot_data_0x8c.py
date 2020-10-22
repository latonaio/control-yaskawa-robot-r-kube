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
            "String": self.STRING_VALUE,
        }

    @property
    def STRING_VALUE(self):
        return self.binary[0:32].decode("utf-8", errors="ignore")

    @STRING_VALUE.setter
    def STRING_VALUE(self, v):
        self._set_bytes(0, v.decode("shift_jis")[0:32])
