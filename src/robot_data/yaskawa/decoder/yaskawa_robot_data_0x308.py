#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from .yaskawa_robot_data import YaskawaRobotData
from .yaskawa_robot_data_0x80 import RobotData as YaskawaRobotData0x80


class RobotData(YaskawaRobotData):
    datas = []  # array of YaskawaRobotData0x80

    def __init__(self, req, res):
        binary = res.get_data()
        count = int.from_bytes(binary[0:4], byteorder=self.byte_order)
        for i in range(count):
            dat = YaskawaRobotData0x80(req, None)
            dat._set_binary(
                binary[i * YaskawaRobotData0x80.DATA_SIZE + 4: (i + 1) * YaskawaRobotData0x80.DATA_SIZE + 4])
            dat.ARRAY_NO = req.ARRAY_NO + i
            self.datas.append(dat)

    def to_json(self):
        return {**self.get_header(), **{"RobotData": self.to_array()}}

    def to_array(self):
        return [data.to_array() for data in self.datas]
