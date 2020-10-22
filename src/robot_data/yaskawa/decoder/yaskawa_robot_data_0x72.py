#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData


class RobotData(YaskawaRobotData):
    data_size = 8

    def to_array(self):
        return {
            "RobotStatus": self.ROBOT_STATUS,
            "ArrayNo": self.array_no,
        }

    @property
    def ROBOT_STATUS(self):
        return [self._byte_to_bits(int.from_bytes(self.binary[0:4], byteorder=self.byte_order)),
                self._byte_to_bits(int.from_bytes(self.binary[4:8], byteorder=self.byte_order))]

    @ROBOT_STATUS.setter
    def ROBOT_STATUS(self, v):
        self._set_bytes(0, self._bits_to_byte(
            v[0]).to_bytes(4, self.byte_order))
        self._set_bytes(4, self._bits_to_byte(
            v[1]).to_bytes(4, self.byte_order))
