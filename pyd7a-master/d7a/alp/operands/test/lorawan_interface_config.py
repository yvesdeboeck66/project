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
import binascii
import pprint
import unittest

from bitstring import ConstBitStream

from d7a.alp.operands.lorawan_interface_configuration_abp import LoRaWANInterfaceConfigurationABP
from d7a.alp.operands.lorawan_interface_configuration_otaa import LoRaWANInterfaceConfigurationOTAA

class TestLoRaWANInterfaceConfiguration(unittest.TestCase):
  def test_byte_generation(self):
    lorawan_config_abp = LoRaWANInterfaceConfigurationABP(
      adr_enabled=True,
      request_ack=True,
      app_port=2,
      data_rate=0,
      netw_session_key=[0] * 16,
      app_session_key=[1] * 16,
      dev_addr=1,
      netw_id=2,
    )
    lorawan_config_otaa = LoRaWANInterfaceConfigurationOTAA(
      adr_enabled=True,
      request_ack=True,
      app_port=2,
      data_rate=0,
      device_eui=[0] * 8,
      app_eui=[0] * 8,
      app_key=[0] * 16
    )


    bytes = bytearray(lorawan_config_abp)
    self.assertEqual(len(bytes), 43)
    self.assertEqual(bytes[0], (1 << 1) + (1 << 2)) # control byte
    self.assertEqual(bytes[1], 2) # app port
    self.assertEqual(bytes[2], 0) # data rate

    self.assertEqual(bytes[3:19], bytearray([0] * 16))  # netw session key
    self.assertEqual(bytes[19:35], bytearray([1] * 16))  # app session key
    self.assertEqual(bytes[35:39], bytearray('\x00\x00\x00\x01'))  # dev addr
    self.assertEqual(bytes[39:43], bytearray('\x00\x00\x00\x02'))  # netw id


    bytes = bytearray(lorawan_config_otaa)
    self.assertEqual(len(bytes), 35)
    self.assertEqual(bytes[0], (1 << 1) + (1 << 2))  # control byte
    self.assertEqual(bytes[1], 2)  # app port
    self.assertEqual(bytes[2], 0) # data rate

    self.assertEqual(bytes[3:11], bytearray([0] * 8))  # device EUI
    self.assertEqual(bytes[11:19], bytearray([0] * 8))  # app EUI
    self.assertEqual(bytes[19:35], bytearray([0] * 16))  # app key


  def test_parsing(self):
    bytes_abp = [
      (1 << 1) + (1 << 2),  # control byte
      2,  # app port
      0, # data rate
    ]

    bytes_abp.extend([0] * 16)  # netw session key
    bytes_abp.extend([1] * 16)  # app session key
    bytes_abp.extend([0, 0, 0, 1])  # dev addr
    bytes_abp.extend([0, 0, 0, 2])  # netw id

    config_abp = LoRaWANInterfaceConfigurationABP.parse(ConstBitStream(bytes=bytes_abp))
    self.assertEqual(type(config_abp), LoRaWANInterfaceConfigurationABP)
    self.assertEqual(config_abp.request_ack, True)
    self.assertEqual(config_abp.adr_enabled, True)
    self.assertEqual(config_abp.app_port, 2)
    self.assertEqual(config_abp.data_rate, 0)
    self.assertEqual(config_abp.netw_session_key, bytearray([0] * 16))
    self.assertEqual(config_abp.app_session_key, bytearray([1] * 16))
    self.assertEqual(config_abp.dev_addr, 1)
    self.assertEqual(config_abp.netw_id, 2)

    bytes_otaa = [
      (1 << 1) + (1 << 2),  # control byte
      2,  # app port
      0, # data rate
    ]

    bytes_otaa.extend([0] * 8)  # device eui
    bytes_otaa.extend([0] * 8)  # app eui
    bytes_otaa.extend([0] * 16)  # app key

    config_otaa = LoRaWANInterfaceConfigurationOTAA.parse(ConstBitStream(bytes=bytes_otaa))
    self.assertEqual(type(config_otaa), LoRaWANInterfaceConfigurationOTAA)
    self.assertEqual(config_otaa.request_ack, True)
    self.assertEqual(config_otaa.adr_enabled, True)
    self.assertEqual(config_otaa.app_port, 2)
    self.assertEqual(config_otaa.data_rate, 0)
    self.assertEqual(config_otaa.device_eui, bytearray([0] * 8))
    self.assertEqual(config_otaa.app_eui, bytearray([0] * 8))
    self.assertEqual(config_otaa.app_key, bytearray([0] * 16))

