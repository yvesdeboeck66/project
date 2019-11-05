#!/usr/bin/env python
#
# Copyright (c) 2015-2019 University of Antwerp, Aloxy NV.
#
# This file is part of pyd7a
# (see https://github.com/MOSAIC-LoPoW/pyd7a).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse
import sys
import logging

from d7a.alp.command import Command

from d7a.phy.channel_id import ChannelID
from d7a.system_files.engineering_mode import EngineeringModeFile, EngineeringModeMode

from modem.modem import Modem

from util.logger import configure_default_logger


def received_command_callback(cmd):
  logging.info(cmd)
  if cmd.execution_completed:
      sys.exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
argparser.add_argument("-c", "--channel-id", help="for example 868LP000 ; format FFFRCIII where FFF={433, 868, 915}, R={L, N, H, R (LORA)}, C={P (PN9), F (FEC), C (CW)} III=000...280", default="868LP000")
modes = ["OFF", "CONT_TX", "TRANSIENT_TX", "PER_RX", "PER_TX"]
argparser.add_argument("-m", "--mode", choices=modes, required=True)
argparser.add_argument("-e", "--eirp", help="EIRP in dBm", type=int, default=0)
argparser.add_argument("-t", "--timeout", help="timeout", type=int, default=0)
config = argparser.parse_args()
configure_default_logger(config.verbose)

ch = ChannelID.from_string(config.channel_id)
print("Using mode {} for channel {} with TX EIRP {} dBm".format(config.mode, config.channel_id, config.eirp))
mode = EngineeringModeMode.from_string(config.mode)

modem = Modem(config.device, config.rate, unsolicited_response_received_callback=received_command_callback)
modem.connect()

emFile = EngineeringModeFile(mode=mode, flags=0, timeout=config.timeout, channel_id=ch, eirp=config.eirp)

modem.execute_command(
  alp_command=Command.create_with_write_file_action(
    file_id=5,
    data=list(emFile),
  )
)

try:
    while True:
        pass
except KeyboardInterrupt:
    sys.exit(0)
