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
import os

import logging

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.lorawan_interface_configuration_otaa import LoRaWANInterfaceConfigurationOTAA
from d7a.alp.operands.lorawan_interface_configuration_abp import LoRaWANInterfaceConfigurationABP

from modem.modem import Modem

# This example can be used with a node running the mode app included in OSS-7, which is connect using the supplied serial device.
# It will send a LoRaWAN message print the result.
from util.logger import configure_default_logger


def received_command_callback(cmd):
  logging.info(cmd)
  if cmd.execution_completed:
    os._exit(0)

argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--device", help="serial device /dev file modem",
                            default="/dev/ttyUSB0")
argparser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
argparser.add_argument("-v", "--verbose", help="verbose", default=False, action="store_true")
argparser.add_argument("-otaa", "--over-the-air-activation", help="Enable over the air activation", default=False, action="store_true")
config = argparser.parse_args()

configure_default_logger(config.verbose)

modem = Modem(config.device, config.rate, )
modem.connect()
logging.info("Executing query...")
if(config.over_the_air_activation):
	result = modem.execute_command(
	  alp_command=Command.create_with_read_file_action(
		file_id=0x40,
		length=8,
		interface_type=InterfaceType.LORAWAN_OTAA,
		interface_configuration=LoRaWANInterfaceConfigurationOTAA(
		  request_ack=False,
		  app_port=0x01,
		  device_eui=[0xBE, 0X7A, 0X00, 0X00, 0X00, 0X00, 0X1B, 0X81],
		  app_eui=[0xBE, 0X7A, 0X00, 0X00, 0X00, 0X00, 0X0D, 0X9F],
		  app_key=[0X7E, 0XEF, 0X56, 0XEC, 0XDA, 0X1D, 0XD5, 0XA4, 0X70, 0X59, 0XFD, 0X35, 0X9C, 0XE6, 0X80, 0XCD],
		  adr_enabled=False,
		  data_rate=0
		)
	  ),
	  timeout_seconds=100
	)

else:
	result = modem.execute_command(
	  alp_command=Command.create_with_read_file_action(
		file_id=0x40,
		length=8,
		interface_type=InterfaceType.LORAWAN_ABP,
		interface_configuration=LoRaWANInterfaceConfigurationABP(
		  request_ack=False,
		  app_port=0x01,
		  netw_session_key=[0x53, 0x1b, 0xd9, 0xc5, 0xec, 0x5d, 0x8b, 0xa5, 0xef, 0x3b, 0x26, 0x2c, 0xeb, 0xfb, 0x3e, 0x66],
		  app_session_key=[0x53, 0x1b, 0xd9,0xc5, 0xec, 0x5d, 0x8b, 0xa5, 0xef, 0x3b, 0x26, 0x2c, 0xeb, 0xfb, 0x3e, 0x66],
		  dev_addr=0x00112233,
		  netw_id=0x000017,
	      adr_enabled=False,
		  data_rate=0
		)
	  ),
	  timeout_seconds=100
	)

try:
	while True:
		pass
except KeyboardInterrupt:
	os._exit(0)
