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

# command line tool to generate ALP messages
# author: Christophe VG <contact@christophe.vg>

import sys
import argparse

from d7a.alp.operations.responses import ReturnFileData

def generate_message(operation, addressee, file, data):
  return bytearray(
    operation.send_command(
      addressee = addressee,
      file      = file,
      data      = data
  ))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="tool to generate ALP messages"
  )

  parser.add_argument("-v", "--verbose", help="be verbose",
                      action='store_true', default=False)
  parser.add_argument("--hex", dest="style",
                      help="display message in hex (default)",
                      action="store_const", const=hex, default=hex)
  parser.add_argument("-i", "--int", dest="style",
                      help="display message in int",
                      action="store_const", const=int)

  def unknown_int(val): return int(val, 0)

  parser.add_argument("addressee", help="the addressee",    type=unknown_int)
  parser.add_argument("file",      help="the file ID",      type=unknown_int)
  parser.add_argument("data",      help="the file content")
  parser.add_argument("more",      help="the file content", nargs="*")
  
  config = parser.parse_args()

  if config.more != []:
    data = [unknown_int(config.data)]
    data.extend(map(unknown_int, config.more))
  else:
    data =  list(bytearray(config.data))

  cmd = generate_message(
    ReturnFileData,
    config.addressee,
    config.file,
    data
  )

  bytes = list(bytearray(cmd))
  if config.verbose:
    print "message size =", len(bytes)

  if config.style == hex:
    [ sys.stdout.write("0x{:02x} ".format(b)) for b in bytes ]
    print
  elif config.style == int:
    print bytes
  