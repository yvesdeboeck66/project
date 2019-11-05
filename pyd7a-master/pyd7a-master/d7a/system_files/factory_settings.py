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
import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.file import File
from d7a.system_files.system_file_ids import SystemFileIds


class FactorySettingsFile(File, Validatable):

  SCHEMA = [{
    "gain": Types.INTEGER(min=-128, max=127),
    "rx_bw_low_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "rx_bw_normal_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "rx_bw_high_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "bitrate_lo_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "fdev_lo_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "bitrate_normal_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "fdev_normal_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "bitrate_hi_rate": Types.INTEGER(min=0, max=0xFFFFFFFF),
    "fdev_hi_rate": Types.INTEGER(min=0, max=0xFFFFFFFF)
  }]

  def __init__(self, gain=0, rx_bw_low_rate=10468, rx_bw_normal_rate=78646, rx_bw_high_rate=125868,
               bitrate_lo_rate=9600, fdev_lo_rate=4800,
               bitrate_normal_rate=55555, fdev_normal_rate=50000, bitrate_hi_rate=166667, fdev_hi_rate=41667):
    self.gain = gain
    self.rx_bw_low_rate = rx_bw_low_rate
    self.rx_bw_normal_rate = rx_bw_normal_rate
    self.rx_bw_high_rate = rx_bw_high_rate
    self.bitrate_lo_rate = bitrate_lo_rate
    self.fdev_lo_rate = fdev_lo_rate
    self.bitrate_normal_rate = bitrate_normal_rate
    self.fdev_normal_rate = fdev_normal_rate
    self.bitrate_hi_rate = bitrate_hi_rate
    self.fdev_hi_rate = fdev_hi_rate
    File.__init__(self, SystemFileIds.FACTORY_SETTINGS, 37)
    Validatable.__init__(self)

  @staticmethod
  def parse(s):
    gain = s.read("int:8")
    rx_bw_low_rate = s.read("uint:32")
    rx_bw_normal_rate = s.read("uint:32")
    rx_bw_high_rate = s.read("uint:32")
    bitrate_lo_rate = s.read("uint:32")
    fdev_lo_rate = s.read("uint:32")
    bitrate_normal_rate = s.read("uint:32")
    fdev_normal_rate = s.read("uint:32")
    bitrate_hi_rate = s.read("uint:32")
    fdev_hi_rate = s.read("uint:32")

    return FactorySettingsFile(gain=gain, rx_bw_low_rate=rx_bw_low_rate, rx_bw_normal_rate=rx_bw_normal_rate, rx_bw_high_rate=rx_bw_high_rate,
                               bitrate_lo_rate=bitrate_lo_rate, fdev_lo_rate=fdev_lo_rate,
                               bitrate_normal_rate=bitrate_normal_rate, fdev_normal_rate=fdev_normal_rate,
                               bitrate_hi_rate=bitrate_hi_rate, fdev_hi_rate=fdev_hi_rate)

  def __iter__(self):
    yield self.gain
    for byte in bytearray(struct.pack(">I", self.rx_bw_low_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.rx_bw_normal_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.rx_bw_high_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.bitrate_lo_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.fdev_lo_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.bitrate_normal_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.fdev_normal_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.bitrate_hi_rate)):
      yield byte
    for byte in bytearray(struct.pack(">I", self.fdev_hi_rate)):
      yield byte

  def __str__(self):
    return "gain={}, rx_bw_low_rate={}, rx_bw_normal_rate={}, rx_bw_high_rate={}, low rate={} : {}, normal rate={} : {}, high rate={} : {}".format(self.gain, hex(self.rx_bw_low_rate), hex(self.rx_bw_normal_rate), hex(self.rx_bw_high_rate),
                                                                                         self.bitrate_lo_rate, self.fdev_lo_rate,
                                                                                         self.bitrate_normal_rate, self.fdev_normal_rate, self.bitrate_hi_rate, self.fdev_hi_rate)