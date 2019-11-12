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
from d7a.fs.file_header import FileHeader
from d7a.support.schema import Validatable, Types


class FileHeaderOperand(Validatable):

  SCHEMA = [{
    "file_id": Types.BYTE(),
    "file_header": Types.OBJECT(FileHeader)
  }]

  def __init__(self, file_id, file_header):
    self.file_id = file_id
    self.file_header = file_header
    super(FileHeaderOperand, self).__init__()

  def __iter__(self):
    yield self.file_id
    for byte in self.file_header: yield byte

  @staticmethod
  def parse(s):
    file_id = s.read("uint:8")
    file_header = FileHeader.parse(s)
    return FileHeaderOperand(file_id=file_id, file_header=file_header)

  def __str__(self):
    return "file-id={}, header={}".format(self.file_id, self.file_header)