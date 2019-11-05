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


class LoRaWANInterfaceConfigurationOTAA(Validatable):

  SCHEMA = [{
    # # TODO first byte is extensible with other fields
    # "adr_enabled": Types.BOOLEAN(),
    # "request_ack": Types.BOOLEAN(),
    # "application_port": Types.BYTE(),
    # "data_rate": Types.BYTE(),
    # "device_eui": Types.BYTES(),
    # "app_eui": Types.BYTES(),
    # "app_key": Types.BYTES()
  }]

  def __init__(self, adr_enabled, request_ack, app_port, data_rate, device_eui, app_eui, app_key):
    self.adr_enabled = adr_enabled
    self.request_ack = request_ack
    self.app_port = app_port
    self.data_rate = data_rate
    self.device_eui = device_eui
    self.app_eui = app_eui
    self.app_key = app_key
    super(LoRaWANInterfaceConfigurationOTAA, self).__init__()

  def __iter__(self):
    byte = 0
    if self.request_ack:
      byte |= 1 << 1

    if self.adr_enabled:
      byte |= 1 << 2

    yield byte
    yield self.app_port
    yield self.data_rate
    
    for byte in self.device_eui:
      yield byte

    for byte in self.app_eui:
      yield byte

    for byte in self.app_key:
      yield byte


  def __str__(self):
    return str(self.as_dict())

  @staticmethod
  def parse(s):
    _rfu = s.read("bits:5")
    adr_enabled = s.read("bool")
    request_ack = s.read("bool")
    _rfu = s.read("bits:1")
    app_port = s.read("uint:8")
    data_rate = s.read("uint:8")
    device_eui = s.read("bytes:8")
    app_eui = s.read("bytes:8")
    app_key = s.read("bytes:16")

    return LoRaWANInterfaceConfigurationOTAA(
      request_ack=request_ack,
      adr_enabled=adr_enabled,
      app_port=app_port,
      data_rate=data_rate,
      device_eui=device_eui,
      app_eui=app_eui,
      app_key=app_key
    )



