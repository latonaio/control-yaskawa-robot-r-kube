#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.


def set_length(val, length):
    if len(val) > length:
        raise ValueError(
            "value is too large (set length: %d, real length: %d)", len(val), length)
    return val.ljust(length, b'\00')


class YaskawaUdpPacket:
    def __init__(self):
        self.binary = bytearray(32)
        # set main header
        index = 0
        index = self.define_property(
            "identify", index, 4, 'YERC'.encode())
        index = self.define_property("header_size", index, 2, 32)
        index = self.define_property("data_size", index, 2, 0)
        index = self.define_property("reserved_1", index, 1, 3)
        index = self.define_property("process_class", index, 1, 1)
        index = self.define_property("ack", index, 1, 0)
        index = self.define_property("request_id", index, 1, 0)
        index = self.define_property("block_no", index, 4, 0)
        self.define_property("reserved_2", index, 8, '99999999'.encode())

    def set_binary(self, binary):
        if binary[0:4] != 'YERC'.encode():
            print("identifier not matched.")
            return False
        self.binary = binary
        return True

    def getter(self, start, length):
        end = start + length
        if len(self.binary) >= end and len(self.binary) >= start > end:
            raise IndexError("out of range")
        return bytes(self.binary[start:end])[::-1]

    def setter(self, start, length, val):
        end = start + length
        if isinstance(val, int):
            self.binary[start:end] = set_length(
                val.to_bytes(length, 'little'), length)
        elif isinstance(val, str):
            self.binary[start:end] = set_length(
                bytes.fromhex(val), length)[::-1]
        elif isinstance(val, bytes):
            self.binary[start:end] = set_length(val, length)
        else:
            raise ValueError("cant set value")

    def define_property(self, name, start, length, initial_value=None):
        end = start + length

        def getter(in_self):
            return in_self.getter(start, length)

        def setter(in_self, value):
            return in_self.setter(start, length, value)

        setattr(self.__class__, name, property(getter, setter))
        self.setter(start, length, initial_value)

        return end

    def get_packet(self):
        return bytes(self.binary)

    def get_data(self):
        if self.header_size is None or self.data_size is None:
            raise IndexError("cant get header size or data size")
        header_size = int(self.header_size.hex(), 16)
        data_size = int(self.data_size.hex(), 16)
        return self.binary[header_size:header_size + data_size]


class SendPacket(YaskawaUdpPacket):
    def __init__(self):
        super().__init__()

        index = 24
        index = self.define_property("command", index, 2, 0)
        index = self.define_property("array_no", index, 2, 0)
        index = self.define_property("element_no", index, 1, 0)
        index = self.define_property("process_no", index, 1, 0)
        self.define_property("padding", index, 2, 1)


class RcvPacket(YaskawaUdpPacket):
    def __init__(self):
        super().__init__()

        index = 24
        index = self.define_property("process_no", index, 1, 0)
        index = self.define_property("status", index, 1, 0)
        index = self.define_property("additional_status_type", index, 1, 0)
        index = self.define_property("padding_1", index, 1, 1)
        index = self.define_property("additional_status_code", index, 2, 0)
        self.define_property("padding_2", index, 2, 0)

    def get_status(self):
        res = {
            "ResponseStatus": self.status.hex(),
        }
        if self.additional_status_type != b'00':
            res["ResponseAdditionalStatus"] = self.additional_status_code.hex()
        return res
