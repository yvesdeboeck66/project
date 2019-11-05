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

from d7a.serial_modem_interface.parser import Parser
from pprint import pprint

cmd = [
  0x20,                                   # action=32/ReturnFileData
  0x40,                                   # File ID
  0x00,                                   # offset
  0x04,                                   # length
  0x00, 0xf3, 0x00, 0x00                  # data
]
    
frame = [
  0xC0,                                   # interface sync byte
  0,                                      # interface version
  len(cmd),                               # ALP cmd length
] + cmd
    
(cmds, info) = Parser().parse(frame)

pprint(cmds[0].as_dict())

print([ "0x{:02x}".format(b) for b in bytearray(cmds[0]) ])
