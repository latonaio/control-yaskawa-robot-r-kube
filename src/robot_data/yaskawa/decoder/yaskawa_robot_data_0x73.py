#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 44

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "JobName": self.job_name,
            "LineNo": self.line_no,
            "StepNo": self.step_no,
            "OverrideSpeed": self.override_speed,
        }

    @property
    def job_name(self):
        return self._string_decoder(self.binary[0:32])

    @job_name.setter
    def job_name(self, v):
        self._set_bytes(0, v.decode(self.encode)[0:32])

    @property
    def line_no(self):
        return int.from_bytes(self.binary[32:36], byteorder=self.byte_order)

    @line_no.setter
    def line_no(self, v):
        self._set_bytes(32, v.to_bytes(4, self.byte_order))

    @property
    def step_no(self):
        return int.from_bytes(self.binary[36:40], byteorder=self.byte_order)

    @step_no.setter
    def step_no(self, v):
        self._set_bytes(36, v.to_bytes(4, self.byte_order))

    @property
    def override_speed(self):
        return int.from_bytes(self.binary[40:44], byteorder=self.byte_order)

    @override_speed.setter
    def override_speed(self, v):
        self._set_bytes(40, v.to_bytes(4, self.byte_order))
