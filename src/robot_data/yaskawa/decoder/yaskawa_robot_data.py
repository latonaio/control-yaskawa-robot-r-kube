#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.


class YaskawaRobotData:
    byte_order = 'little'
    encode = "shift_jis"
    data_size = 0  # ファイル上の1データのサイズ
    status = {}
    command = ""

    def __init__(self, req, res):
        if res:
            self.status = res.get_status()
            self._set_binary(res.get_data())
        else:
            self._set_binary(bytes(self.data_size))
        if req:
            self.array_no = int.from_bytes(req.array_no, byteorder="big")
            self.command = req.command.hex()

    def _set_binary(self, binary):
        self.binary = binary

    def _set_bytes(self, pos, value):
        data = bytearray(self.binary)
        data[pos:pos + len(value)] = value
        self.binary = bytes(data)

    def is_success(self):
        return True if self.status and self.status.get("ResponseStatus") == "00" else False

    def to_array(self):
        return {}

    def get_status(self):
        return {"ArrayNo": self.array_no, **self.status}

    def _string_decoder(self, byte):
        return byte.decode(self.encode).replace("\x00", "")

    @staticmethod
    def _byte_to_bits(value):
        return [int(s) for s in format(value, '08b')][::-1]

    @staticmethod
    def _bits_to_byte(values):
        return (values[0] & 0b1) << 0 | (values[1] & 0b1) << 1 | (values[2] & 0b1) << 2 | (values[3] & 0b1) << 3 | (
                values[4] & 0b1) << 4 | (values[5] & 0b1) << 5 | (values[6] & 0b1) << 6 | (values[7] & 0b1) << 7


class YaskawaRobotDataList:
    def __init__(self, command, expire_time, robot_data_list):
        self.expire_time = expire_time
        self.data_list = robot_data_list
        if isinstance(command, bytes):
            command = command.hex()
        self.command = command
        self.is_success = all([d.is_success() for d in self.data_list])

    def get_header(self):
        return {
            "Command": self.command,
            "Result": self.is_success,
            "ExpireTime": self.expire_time,
            "BaseObjectType": "TosouMotomachi",
            "ComponentType": "SentouLine",
            "MotionDeviceSystemType": "RobotDataCollections",
            "MotionDeviceIdentifier": "YR-923756",
            "MotionDeviceType": "MOTOMAN-MPX1150",
            "ComponentName": "MOTOMAN-MPX1150",
            "Manufacturer": "Yaskawa",
            "Model": "MOTOMAN-MPX",
            "DataForm": "32bit_integer",
        }

    def to_json(self):
        robot_data_list = [d.to_array() if d.is_success() else d.get_status() for d in self.data_list]
        return {**self.get_header(), **{"RobotData": robot_data_list}}
