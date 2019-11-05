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

# author: Christophe VG <contact@christophe.vg>
# unit tests for the D7 ALP parser

import unittest

from bitstring import ConstBitStream

from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file_header import FileHeaderOperand
from d7a.alp.operands.indirect_interface_operand import IndirectInterfaceOperand
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.operands.lorawan_interface_configuration_abp import LoRaWANInterfaceConfigurationABP
from d7a.alp.operands.lorawan_interface_configuration_otaa import LoRaWANInterfaceConfigurationOTAA
from d7a.alp.operands.query import QueryOperand
from d7a.alp.operations.forward import Forward

from d7a.alp.parser import Parser
from d7a.d7anp.addressee import Addressee, IdType
from d7a.parse_error import ParseError
from d7a.phy.channel_header import ChannelBand, ChannelCoding, ChannelClass


class TestParser(unittest.TestCase):
  def setUp(self):
    self.interface_status_action = [
      0x62,                                           # Interface Status action
      0xD7,                                           # D7ASP interface
      32,                                              # channel_header
      0, 0,                                           # channel_id
      0,                                              # rxlevel (- dBm)
      0,                                              # link budget
      80,                                             # target rx level
      0,                                              # status
      0,                                              # fifo token
      0,                                              # seq
      0,                                              # response timeout
      1 << 4,                                         # addressee ctrl (NOID, nls_method=NONE)
      0                                               # access class
    ]

  def test_basic_valid_message(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ] + self.interface_status_action

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length.value, 4)

  def test_basic_valid_message_actions_swapped(self):
    cmd_data = self.interface_status_action + [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length.value, 4)

  def test_command_without_interface_status(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xfF, 0x00, 0x00                          # data
      # missing interface status action!
    ]
    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.interface_status, None)

  def test_command_with_multiple_interface_status_actions(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ] + self.interface_status_action + self.interface_status_action # <- 2x interface_status!
    with self.assertRaises(ParseError):
      cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))

  def test_empty_data(self):
    alp_action_bytes = [
      0x20,
      0x40,
      0x00,
      0x00
    ]

    parser = Parser()
    cmd = parser.parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(len(cmd.actions[0].operation.operand.data), 0)

  def test_unsupported_action(self):
    alp_action_bytes = [
      0x25,
      0x40,
      0x00,
      0x00
    ]
    with self.assertRaises(ParseError):
      cmd = Parser().parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))

  def test_multiple_actions(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00,                         # data
    ]

    cmd_bytes = alp_action_bytes + alp_action_bytes + self.interface_status_action
    cmd = Parser().parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length.value, 4)
    self.assertEqual(cmd.actions[1].operation.op, 32)
    self.assertEqual(cmd.actions[1].operation.operand.length.value, 4)

  def test_multiple_non_grouped_actions_in_command(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]

    cmd_bytes = alp_action_bytes + alp_action_bytes + self.interface_status_action
    cmd = Parser().parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))

    self.assertEqual(len(cmd.actions), 2)
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length.value, 4)
    self.assertEqual(cmd.actions[1].operation.op, 32)
    self.assertEqual(cmd.actions[1].operation.operand.length.value, 4)

  # TODO not implemented yet
  # def test_multiple_grouped_actions_in_command(self):
  #   alp_action_first_in_group_bytes = [
  #     0xa0,                                           # action=32/ReturnFileData  + grouped flag
  #     0x40,                                           # File ID
  #     0x00,                                           # offset
  #     0x04,                                           # length
  #     0x00, 0xf3, 0x00, 0x00                          # data
  #   ]
  #   alp_action_second_in_group_bytes = [
  #     0x20,                                           # action=32/ReturnFileData
  #     0x40,                                           # File ID
  #     0x00,                                           # offset
  #     0x04,                                           # length
  #     0x00, 0xf3, 0x00, 0x00                          # data
  #   ]
  #   (cmds, info) = self.parser.parse([
  #     0xc0, 0, len(alp_action_first_in_group_bytes) + len(alp_action_second_in_group_bytes)
  #   ] + alp_action_first_in_group_bytes + alp_action_second_in_group_bytes)
  #
  #   self.assertEqual(len(cmds), 1)
  #   self.assertEqual(len(cmds[0].actions), 2)
  #   self.assertEqual(cmds[0].actions[0].operation.op, 32)
  #   self.assertEqual(cmds[0].actions[0].operation.operand.length, 4)
  #   self.assertEqual(cmds[0].actions[0].group, True)
  #   self.assertEqual(cmds[0].actions[1].operation.op, 32)
  #   self.assertEqual(cmds[0].actions[1].operation.operand.length, 4)
  #   self.assertEqual(cmds[0].actions[0].group, False)

  def test_interface_status_action_d7asp(self):
    alp_action_bytes = [
      34 + 0b01000000,                                 # action=34 + inf status
      0xd7,                                           # interface ID
      32,                                           # channel_header
      0, 16,                                          # channel_index
      70,                                             # rx level
      80,                                             # link budget
      80,                                             # target rx level
      0,                                              # status
      0xa5,                                           # fifo token
      0x00,                                           # request ID
      20,                                             # response timeout
      0b00100010,                                     # addr control
      5,                                              # access class
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # addr
    ]

    cmd = Parser().parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))
    self.assertIsNotNone(cmd.interface_status)
    self.assertEqual(cmd.interface_status.op, 34)
    self.assertEqual(type(cmd.interface_status.operand), InterfaceStatusOperand)
    self.assertEqual(cmd.interface_status.operand.interface_id, 0xD7)
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_id.channel_header.channel_band, ChannelBand.BAND_433)
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_id.channel_header.channel_coding, ChannelCoding.PN9)
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_id.channel_header.channel_class, ChannelClass.LO_RATE)
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_id.channel_index, 16)
    self.assertEqual(cmd.interface_status.operand.interface_status.rx_level, 70)
    self.assertEqual(cmd.interface_status.operand.interface_status.link_budget, 80)
    self.assertEqual(cmd.interface_status.operand.interface_status.missed, False)
    self.assertEqual(cmd.interface_status.operand.interface_status.nls, False)
    self.assertEqual(cmd.interface_status.operand.interface_status.seq_nr, 0)
    self.assertEqual(cmd.interface_status.operand.interface_status.response_to.exp, 0)
    self.assertEqual(cmd.interface_status.operand.interface_status.response_to.mant, 20)
    self.assertEqual(cmd.interface_status.operand.interface_status.retry, False)

  #def test_interface_status_action_unknown_interface(self):
    # TODO 


  def test_without_tag_request(self):
    cmd_data = [
                 0x20,  # action=32/ReturnFileData
                 0x40,  # File ID
                 0x00,  # offset
                 0x04,  # length
                 0x00, 0xf3, 0x00, 0x00  # data
               ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.tag_id, None) # a random ID will not be generated

  def test_with_tag_request(self):
    cmd_data = [
                 52,    # action=TagRequest, without EOP bit set
                 14,    # tag ID
                 0x20,  # action=32/ReturnFileData
                 0x40,  # File ID
                 0x00,  # offset
                 0x04,  # length
                 0x00, 0xf3, 0x00, 0x00  # data
               ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.tag_id, 14)
    self.assertEqual(cmd.send_tag_response_when_completed, False)


  def test_with_tag_request_EOP_bit_set(self):
    action = 52
    action |= 1 << 7
    cmd_data = [
                 action,    # action=TagRequest, withEOP bit set
                 14,    # tag ID
                 0x20,  # action=32/ReturnFileData
                 0x40,  # File ID
                 0x00,  # offset
                 0x04,  # length
                 0x00, 0xf3, 0x00, 0x00  # data
               ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.tag_id, 14)
    self.assertEqual(cmd.send_tag_response_when_completed, True)

  def test_with_multiple_tag_requests(self):
    cmd_data = [
      52,  # action=TagRequest, without EOP bit set
      14,  # tag ID
      52,  # another TagRequest while only 1 per command supported
      15,  # tag ID
      0x20,  # action=32/ReturnFileData
      0x40,  # File ID
      0x00,  # offset
      0x04,  # length
      0x00, 0xf3, 0x00, 0x00  # data
    ]

    with self.assertRaises(ParseError):
      cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))

  def test_return_file_header(self):
    cmd_data = [ 0x21, 0x02, 0x00, 0x03, 0x00, 0x00, 0x0F, 0x00, 0x00,  0x00, 0x0F, 0x00, 0x00,  0x00 ]
    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operand), FileHeaderOperand)
    self.assertEqual(cmd.actions[0].operand.file_id, 2)
    self.assertEqual(cmd.actions[0].operand.file_header.properties.act_enabled, False)

  def test_indirect_fwd(self):
    cmd_data = [
      51, # indirect fwd, no overload
      64  # interface file id
    ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operand), IndirectInterfaceOperand)
    self.assertEqual(cmd.actions[0].overload, False)
    self.assertEqual(cmd.actions[0].operand.interface_file_id, 64)
    self.assertEqual(cmd.actions[0].operand.interface_configuration_overload, None)

  def test_indirect_fwd_with_overload(self):
    cmd_data = [
      (1 << 7) + 51, # indirect fwd, no overload
      64, # interface file id
      1 << 4,  # addressee ctrl (NOID, nls_method=NONE)
      0  # access class
    ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operand), IndirectInterfaceOperand)
    self.assertEqual(cmd.actions[0].overload, True)
    self.assertEqual(cmd.actions[0].operand.interface_file_id, 64)
    self.assertEqual(type(cmd.actions[0].operand.interface_configuration_overload), Addressee)
    self.assertEqual(cmd.actions[0].operand.interface_configuration_overload.id_type, IdType.NOID)

  def test_break_query(self):
    cmd_data = [
      9, # break query
      0x44,  # arith comp with value, no mask, unsigned, >
      0x01,  # compare length
      25,  # compare value
      0x20, 0x01  # file offset
    ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operand), QueryOperand)

  def test_break_query(self):
    cmd_data = [
      9, # break query
      0x44,  # arith comp with value, no mask, unsigned, >
      0x01,  # compare length
      25,  # compare value
      0x20, 0x01  # file offset
    ]

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operand), QueryOperand)

  def test_parse_forward_LoRaWAN_iface_ABP(self):
    lorawan_config = LoRaWANInterfaceConfigurationABP(
      adr_enabled=True,
      request_ack=True,
      app_port=0x01,
      data_rate=0,
      netw_session_key=[0] * 16,
      app_session_key=[1] * 16,
      dev_addr=1,
      netw_id=2,
    )

    #bytes = bytearray(lorawan_config)

    bytes = [
      50,  # forward
      0x02,  # LoRaWAN iface id
    ]

    bytes.extend(bytearray(lorawan_config))

    cmd = Parser().parse(ConstBitStream(bytes=bytes), len(bytes))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operation), Forward)
    self.assertEqual(type(cmd.actions[0].operand), InterfaceConfiguration)
    self.assertEqual(cmd.actions[0].operand.interface_id, InterfaceType.LORAWAN_ABP)
    self.assertEqual(type(cmd.actions[0].operand.interface_configuration), LoRaWANInterfaceConfigurationABP)

  def test_parse_forward_LoRaWAN_iface_OTAA(self):
    lorawan_config = LoRaWANInterfaceConfigurationOTAA(
      adr_enabled=True,
      request_ack=True,
      app_port=0x01,
      data_rate=0,
      device_eui=[0] * 8,
      app_eui=[0] * 8,
      app_key=[0] * 16
    )

    #bytes = bytearray(lorawan_config)

    bytes = [
      50,  # forward
      0x03,  # LoRaWAN iface id
    ]

    bytes.extend(bytearray(lorawan_config))

    cmd = Parser().parse(ConstBitStream(bytes=bytes), len(bytes))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(type(cmd.actions[0].operation), Forward)
    self.assertEqual(type(cmd.actions[0].operand), InterfaceConfiguration)
    self.assertEqual(cmd.actions[0].operand.interface_id, InterfaceType.LORAWAN_OTAA)
    self.assertEqual(type(cmd.actions[0].operand.interface_configuration), LoRaWANInterfaceConfigurationOTAA)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
