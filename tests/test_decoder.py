#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import pytest
import yaskawa.udp_packet
from importlib import import_module
from glob import glob
import re
import os
import yaskawa.decoder.yaskawa_robot_data as rd


def get_send_receive_data():
    receive_data_list = glob(os.getcwd() + f"/data/receive/0x*_r.bin")
    assert receive_data_list

    for receive_file in receive_data_list:
        command = re.split("[./]", receive_file)[-2].split("_")[0]
        assert command

        send_data_list = glob(os.getcwd() + f"/data/send/{command}*_s.bin")
        assert send_data_list
        send_file = send_data_list[0]

        with open(receive_file, "rb") as f:
            receive_data = f.read()
        receive_packet = yaskawa.udp_packet.RcvPacket()
        receive_packet.set_binary(receive_data)

        with open(send_file, "rb") as f:
            send_data = f.read()
        send_packet = yaskawa.udp_packet.SendPacket()
        send_packet.set_binary(send_data)

        robot_data_library = import_module("yaskawa.decoder.yaskawa_robot_data_" + command)
        decoder = robot_data_library.RobotData
        yield send_packet, receive_packet, decoder


def test_normal_001_decode_command():
    for send_packet, receive_packet, decoder in get_send_receive_data():
        robot_data = decoder(send_packet, receive_packet)
        assert robot_data


def test_normal_001_robot_list():
    for send_packet, receive_packet, decoder in get_send_receive_data():
        robot_data = decoder(send_packet, receive_packet)
        data_list = rd.YaskawaRobotDataList(send_packet.command, [robot_data])
        assert data_list.to_json()
        print(f"\n> command: {send_packet.command}, array no: {send_packet.array_no}")
        print(data_list.to_json())




