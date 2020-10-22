#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import pytest
import yaskawa.udp_packet


def test_normal_001_setattr():
    packet = yaskawa.udp_packet.YaskawaUdpPacket()
    packet.identify = 'test'.encode()
    assert packet.identify == 'test'.encode()
    packet.identify = '0f'
    assert packet.identify == b'\x00\x00\x00\x0f'
    packet.identify = 32
    assert packet.identify == b'\x20'.rjust(4, b'\x00')


def test_abnormal_001_setattr():
    packet = yaskawa.udp_packet.YaskawaUdpPacket()
    with pytest.raises(ValueError):
        packet.identify = 'testaaa'.encode()
    with pytest.raises(ValueError):
        packet.identify = 0.12
