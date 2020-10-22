#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import pytest
import glob
import yaskawa.command
import yaskawa.udp_packet
import asyncio
import os

TEST_JSON_PATH = "./data/command_list_test.json"
DEFAULT_JSON_PATH = "../data/command_list.json"
TEST_INVALID_JSON_PATH = "./data/command_list_test_invalid.json"
HOST = "127.0.0.1"
PORT = 10101
BUF_SIZE = 4896
TIMEOUT_INTERVAL = 1


class UDPServer:
    def __init__(self, on_receive, count):
        self.transport = None
        self.on_receive = on_receive
        self.resp = []
        self.resp_count = count

    def connection_made(self, transport):
        print("[server] create connection")
        self.transport = transport

    def datagram_received(self, data, addr):
        print("[server] received: ", data.hex())
        if data == b'':
            return

        command = data[24:26][::-1].hex().lstrip("0")
        file_list = glob.glob(os.getcwd() + f"/data/receive/0x{command}*.bin")
        print("[server]", os.getcwd() + f"/data/receive/0x{command}*.bin")

        packet = None
        if not file_list:
            raise FileNotFoundError("[server] test response data is not found")
        with open(file_list[0], "rb") as f:
            packet = f.read()
        if self.transport is not None and packet is not None:
            self.transport.sendto(packet, addr)

        self.resp.append(data)
        if len(self.resp) >= self.resp_count:
            self.on_receive.set_result(self.resp)


def test_normal_read_json():
    conf = yaskawa.command.read_config_json(TEST_JSON_PATH)
    assert conf is not None


def test_abnormal_001_read_json():
    conf = yaskawa.command.read_config_json("a")
    assert conf is None


def test_abnormal_002_read_json():
    conf = yaskawa.command.read_config_json(TEST_INVALID_JSON_PATH)
    assert conf is None


def test_normal_001_create_header():
    conf = yaskawa.command.read_config_json(TEST_JSON_PATH)
    assert conf is not None
    assert len(conf) == 2
    for data in conf:
        res = yaskawa.command.create_header(data)
        assert res
        for key, header in res.items():
            assert header is not None
            assert len(header.get_packet()) == 32
            assert header.identify == b'YERC'[::-1]
            assert header.header_size == b'\x00\x20'
            assert header.reserved_2 == '99999999'.encode()
            header.reserved_2 = b'\x01'
            assert header.reserved_2 == b'\x01'.rjust(8, b'\x00')


def test_normal_001_get_all_header_list_by_json():
    header_list = yaskawa.command.get_all_header_list_by_json(TEST_JSON_PATH)
    assert header_list
    for k, val in header_list.items():
        assert isinstance(val.get("interval"), int)
        assert val.get("headers")
        for key, header in val.get("headers").items():
            assert len(header.get_packet()) == 32


def test_normal_001_send_to_robot():
    loop = asyncio.get_event_loop()

    y = yaskawa.command.YaskawaRobotCommunicator(TEST_JSON_PATH, HOST, PORT, loop)
    count = ((1 / 1) * 2 + (1 / 0.1) * 1) * TIMEOUT_INTERVAL

    on_receive = loop.create_future()
    server = loop.create_datagram_endpoint(
        lambda: UDPServer(on_receive, count), local_addr=(HOST, PORT))
    asyncio.ensure_future(server)

    for command, header_data in y.header_list.items():
        asyncio.ensure_future(y.set_queue_by_interval(command, header_data))
    asyncio.ensure_future(y.send_request())

    loop.run_until_complete(asyncio.wait_for(on_receive, TIMEOUT_INTERVAL))


def test_normal_002_send_to_robot():
    loop = asyncio.get_event_loop()

    y = yaskawa.command.YaskawaRobotCommunicator(DEFAULT_JSON_PATH, HOST, PORT, loop)
    count = TIMEOUT_INTERVAL * 10 / 0.1

    on_receive = loop.create_future()
    server = loop.create_datagram_endpoint(
        lambda: UDPServer(on_receive, count), local_addr=(HOST, PORT))
    asyncio.ensure_future(server)

    for command, header_data in y.header_list.items():
        asyncio.ensure_future(y.set_queue_by_interval(command, header_data))
    asyncio.ensure_future(y.send_request())

    loop.run_until_complete(asyncio.wait_for(on_receive, TIMEOUT_INTERVAL * 10))

"""
def test_normal_001_get_response():
    loop = asyncio.get_event_loop()

    y = yaskawa.command.YaskawaRobotCommunicator(TEST_JSON_PATH, HOST, PORT, loop)
    on_receive = loop.create_future()

    async def set_result_to_on_receive(f):
        f.set_result(True)

    asyncio.ensure_future(set_result_to_on_receive(on_receive))
    loop.run_until_complete(asyncio.wait_for(y.rcv_queue.get(), TIMEOUT_INTERVAL))
"""
