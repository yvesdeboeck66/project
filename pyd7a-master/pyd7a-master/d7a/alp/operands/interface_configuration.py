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
from d7a.alp.interface import InterfaceType
from d7a.support.schema import Validatable, Types


class InterfaceConfiguration(Validatable):
  SCHEMA = [{
    "interface_id"        : Types.ENUM(InterfaceType),
    "interface_configuration"    : Types.OBJECT(Validatable, nullable=True)
  }]

  def __init__(self, interface_id, interface_configuration=None):
    self.interface_id = interface_id
    self.interface_configuration   = interface_configuration
    super(InterfaceConfiguration, self).__init__()

  def __iter__(self):
    yield self.interface_id.value
    if self.interface_configuration:
      for byte in self.interface_configuration: yield byte

  def __str__(self):
    return "interface-id={}, configuration={}".format(self.interface_id, self.interface_configuration)
