#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 28

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "StartTime": self.start_time,
            "ElapsedTime": self.elapsed_time,
        }

    @property
    def start_time(self):
        return self._string_decoder(self.binary[0:16])

    @start_time.setter
    def start_time(self, v):
        self._set_bytes(0, v.decode(self.encode)[0:16])

    @property
    def elapsed_time(self):
        return self._string_decoder(self.binary[16:28])

    @elapsed_time.setter
    def elapsed_time(self, v):
        self._set_bytes(16, v.decode(self.encode)[0:12])
