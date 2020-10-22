#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import asyncio
import os
from time import sleep
from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, lprint_exception

from .yaskawa import command

SERVICE_NAME = "control-yaskawa-robot-r"
ADDRESS = "192.168.2.1"
PORT = 10040
JSON_PATH = os.path.join(
    "/var/lib/aion/Data/control-yaskawa-robot-r_1/command_list.json")
TRIGGER_PATH = os.path.join(
    "/var/lib/aion/Data/control-yaskawa-robot-r_1/trigger_list.json")


@main_decorator(SERVICE_NAME)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()

    kanban = conn.set_kanban(SERVICE_NAME, num)
    address = os.environ[f"ROBOT_IP_{num:02d}"]
    lprint(f"robot address: {address}")

    loop = asyncio.get_event_loop()
    y = command.YaskawaRobotCommunicator(
        JSON_PATH, address, PORT, loop, __file__, TRIGGER_PATH
    )
    y.start_to_send(conn)
