#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 184

    def __init__(self, req, res):
        super().__init__(req, res)

    def to_array(self):
        return {
            "ArrayNo": self.array_no,
            "AlarmCode": self.ALARM_CODE,
            "AlarmData": self.ALARM_DATA,
            "AlarmType": self.ALARM_TYPE,
            "AlarmTime": self.ALARM_TIME,
            "AlarmName": self.ALARM_NAME,
            "SubCodeExtended": self.SUB_CODE_EXTENDED,
            "SubCodeData": self.SUB_CODE_DATA,
            "SubCodeReversedInfo": self.SUB_CODE_REVERSED_INFO,
        }

    @property
    def ALARM_CODE(self):
        return int.from_bytes(self.binary[0:4], byteorder=self.byte_order)

    @ALARM_CODE.setter
    def ALARM_CODE(self, v):
        self._set_bytes(0, v.to_bytes(4, self.byte_order))

    @property
    def ALARM_DATA(self):
        return int.from_bytes(self.binary[4:8], byteorder=self.byte_order)

    @ALARM_DATA.setter
    def ALARM_DATA(self, v):
        self._set_bytes(4, v.to_bytes(4, self.byte_order))

    @property
    def ALARM_TYPE(self):
        return int.from_bytes(self.binary[8:12], byteorder=self.byte_order)

    @ALARM_TYPE.setter
    def ALARM_TYPE(self, v):
        self._set_bytes(8, v.to_bytes(4, self.byte_order))

    @property
    def ALARM_TIME(self):
        return self.binary[12:28].decode("utf-8", errors="ignore")

    @ALARM_TIME.setter
    def ALARM_TIME(self, v):
        self._set_bytes(12, v.decode("shift_jis")[0:16])

    @property
    def ALARM_NAME(self):
        return self.binary[28:60].decode("utf-8", errors="ignore")

    @ALARM_NAME.setter
    def ALARM_NAME(self, v):
        self._set_bytes(28, v.decode("shift_jis")[0:32])

    @property
    def SUB_CODE_EXTENDED(self):
        return self.binary[60:76].decode("utf-8", errors="ignore")

    @SUB_CODE_EXTENDED.setter
    def SUB_CODE_EXTENDED(self, v):
        self._set_bytes(60, v.decode("shift_jis")[0:16])

    @property
    def SUB_CODE_DATA(self):
        return self.binary[76:172].decode("utf-8", errors="ignore")

    @SUB_CODE_DATA.setter
    def SUB_CODE_DATA(self, v):
        self._set_bytes(76, v.decode("shift_jis")[0:96])

    @property
    def SUB_CODE_REVERSED_INFO(self):
        bits = []
        for i in range(172, 184):
            bits.extend(self._byte_to_bits(self.binary[i]))
        return bits

    @SUB_CODE_REVERSED_INFO.setter
    def SUB_CODE_REVERSED_INFO(self, v):
        for i in range(len(v)):
            self._set_bytes(184 + i, self._bits_to_byte(v[i * 8:i * 8 + 8]))
