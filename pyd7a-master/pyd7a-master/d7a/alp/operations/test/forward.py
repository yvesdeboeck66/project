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
import unittest

from bitstring import ConstBitStream
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operands.lorawan_interface_configuration_abp import LoRaWANInterfaceConfigurationABP
from d7a.alp.operands.lorawan_interface_configuration_otaa import LoRaWANInterfaceConfigurationOTAA
from d7a.alp.operations.forward import Forward
from d7a.sp.configuration import Configuration


class TestForward(unittest.TestCase):
  def test_byte_generation_forward_D7A_iface(self):
    d7asp_config = Configuration()
    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=d7asp_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(d7asp_config)) + 1)
    self.assertEqual(bytes[0], 0xD7)
    self.assertEqual(bytes[1:], bytearray(d7asp_config))
    # TODO configuration

  def test_byte_generation_forward_LoRaWAN_ABP_iface(self):
    lorawan_config = LoRaWANInterfaceConfigurationABP(
      adr_enabled=True,
      request_ack=False,
      app_port=0x01,
      data_rate=0,
      netw_session_key=[0x53, 0X1b, 0Xd9, 0Xc5, 0Xec, 0X5d, 0X8b, 0Xa5, 0Xef, 0X3b, 0X26, 0X2c, 0Xeb, 0Xfb, 0X3e, 0X66],
      app_session_key=[0x53, 0X1b, 0Xd9, 0Xc5, 0Xec, 0X5d, 0X8b, 0Xa5, 0Xef, 0X3b, 0X26, 0X2c, 0Xeb, 0Xfb, 0X3e, 0X66],
      dev_addr=1,
      netw_id=2,
    )

    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.LORAWAN_ABP,
        interface_configuration=lorawan_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(lorawan_config)) + 1)
    self.assertEqual(bytes[0], 0x02)
    self.assertEqual(bytes[1:], bytearray(lorawan_config))

  def test_byte_generation_forward_LoRaWAN_OTAA_iface(self):
    lorawan_config = LoRaWANInterfaceConfigurationOTAA(
      adr_enabled=True,
      request_ack=False,
      app_port=0x01,
      data_rate=0,
      device_eui=[0xBE, 0X7A, 0X00, 0X00, 0X00, 0X00, 0X1B, 0X81],
      app_eui=[0xBE, 0X7A, 0X00, 0X00, 0X00, 0X00, 0X0D, 0X9F],
      app_key=[0X7E, 0XEF, 0X56, 0XEC, 0XDA, 0X1D, 0XD5, 0XA4, 0X70, 0X59, 0XFD, 0X35, 0X9C, 0XE6, 0X80, 0XCD]
    )

    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.LORAWAN_OTAA,
        interface_configuration=lorawan_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(lorawan_config)) + 1)
    self.assertEqual(bytes[0], 0x03)
    self.assertEqual(bytes[1:], bytearray(lorawan_config))



