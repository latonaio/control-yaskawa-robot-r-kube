#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 60

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "AlarmCode": self.alarm_code,
            "AlarmData": self.alarm_data,
            "AlarmType": self.alarm_type,
            "AlarmTime": self.alarm_time,
            "AlarmName": self.alarm_name,
        }

    @property
    def alarm_code(self):
        return int.from_bytes(self.binary[0:4], byteorder=self.byte_order)

    @alarm_code.setter
    def alarm_code(self, v):
        self._set_bytes(0, v.to_bytes(4, self.byte_order))

    @property
    def alarm_data(self):
        return int.from_bytes(self.binary[4:8], byteorder=self.byte_order)

    @alarm_data.setter
    def alarm_data(self, v):
        self._set_bytes(4, v.to_bytes(4, self.byte_order))

    @property
    def alarm_type(self):
        return int.from_bytes(self.binary[8:12], byteorder=self.byte_order)

    @alarm_type.setter
    def alarm_type(self, v):
        self._set_bytes(8, v.to_bytes(4, self.byte_order))

    @property
    def alarm_time(self):
        return self._string_decoder(self.binary[12:28])

    @alarm_time.setter
    def alarm_time(self, v):
        self._set_bytes(12, v.decode(self.encode)[0:16])

    @property
    def alarm_name(self):
        return self._string_decoder(self.binary[28:60])

    @alarm_name.setter
    def alarm_name(self, v):
        self._set_bytes(28, v.decode(self.encode)[0:32])
