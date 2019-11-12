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
from d7a.d7anp.addressee import IdType, NlsMethod
from d7a.support.schema import Validatable, Types

class Control(Validatable):

  SCHEMA = [{
    "has_no_origin_access_id": Types.BOOLEAN(),
    "has_hopping": Types.BOOLEAN(),
    "origin_id_type": Types.ENUM(IdType, allowedvalues=[IdType.UID, IdType.VID]),
    "nls_method": Types.ENUM(NlsMethod),
  }]

  def __init__(self, has_no_origin_access_id, has_hopping, nls_method, origin_id_type):
    self.has_no_origin_access_id = has_no_origin_access_id
    self.nls_method = nls_method
    self.has_hopping = has_hopping
    self.origin_id_type = origin_id_type
    super(Control, self).__init__()

  @staticmethod
  def parse(bitstream):
    return Control(
      has_no_origin_access_id=bitstream.read("bool"),
      has_hopping=bitstream.read("bool"),
      origin_id_type=IdType(bitstream.read("uint:2")),
      nls_method=NlsMethod(bitstream.read("uint:4")),
    )

  def __iter__(self):
    byte = 0
    if self.has_no_origin_access_id: byte |= 1 << 7
    if self.has_multi_hop:  byte |= 1 << 6
    if self.origin_id_type:  byte |= 1 << 4
    byte += self.nls_method
    yield byte